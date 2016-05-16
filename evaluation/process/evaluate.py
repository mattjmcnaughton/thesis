"""
evaluation.py contains code for donwloading data from the InfluxDB database
instance, processing it to get graphs and statistical measures comparing the
difference for the summation of eru and qos for predictive vs reactive. It then
outputs the graphs and statistical measurements to the specified output
directory.
"""

# pylint: disable=import-error, too-many-locals, no-self-use, invalid-name

import argparse
import datetime
import json
import os

import numpy
import scipy.stats
import matplotlib.pyplot as plot

from influxdb import InfluxDBClient
from jinja2 import Template

class Evaluate(object):
    """
    Evaluate initializes with a pod initialization time and a traffic pattern. It
    retrieves both the predictive and reactive data from InfluxDB, sums eru and
    qos, and then produces graphs and summary statistics.

    Args:
        pit (str): The pod initialization time tag.
        tp (str): The traffic pattern tag.
        version (str): The version of trials we are running.
        output (str): The directory to which to write output.
    """

    PREDICTIVE = "predictive"
    REACTIVE = "reactive"

    # The possible values that we can query for. Because of the way group by
    # works in influx, it seems like we have to query for each of these values
    # separately and then match them up later.
    # @TODO Add more of these for `time` and `mean`.
    POSSIBLE_VALUES = ["eru", "qos"]

    # Constants for whether the file type is a GRAPH or STATS.
    GRAPH = "graph"
    STATS = "stats"

    # If no version is specified, assume that it is v1.
    DEFAULT_VERSION = "v1"

    def __init__(self, pit, tp, version, output, only_eru, only_qos):
        self._pit = pit
        self._tp = tp
        self._version = version
        self._output = output
        self._only_eru = only_eru
        self._only_qos = only_qos
        self._client = None

    def _get_client(self):
        """
        A singleton method to return an instance of the InfluxDB
        client intialized to access our influxdb database.

        Returns:
            InfluxDBClient: An instance of the InfluxDBClient.
        """
        if self._client is None:
            self._client = InfluxDBClient(host=os.environ["DATABASE_ADDRESS"],
                                          port=os.environ["DATABASE_PORT"],
                                          username=os.environ["DATABASE_USERNAME"],
                                          password=os.environ["DATABASE_PASSWORD"],
                                          database=os.environ["DATABASE_NAME"],
                                          ssl=True)

        return self._client

    def _get_base_query(self, version):
        """
        Return the base influx db query which will be used by any instance of
        this class.

        @TODO Handle versioning of queries better.

        Args:
            version (str): At this point, different versions of trials require
            different queries which isn't ideal, but its what's happening for
            now.

        Returns:
            str: The base influxdb query, which still has fields that need to be
            filled in, but has all instance consistent fields filled in.
        """
        # @TODO Right now this assumes tests were run in the last 10d, which sames
        # like a fairly safe assumption, but is an assumption all the same.
        # @TODO Abstract the specific variable names like `sm`, `tp` as class
        # variables so they aren't just random strings.
        if version == self.DEFAULT_VERSION:
            query = ("SELECT MEAN({{ value }}) from METRICS where time > now() - 40d and "
                     "sm = '{{ sm }}' and pit = '{{ pt }}' and tp = '{{ tp }}' "
                     "and ver !~ /v*/ group by time(1m)")
        else:
            query = ("SELECT MEAN({{ value }}) from METRICS where time > now() - 10d and "
                     "sm = '{{ sm }}' and pit = '{{ pt }}' and tp = '{{ tp }}' "
                     "and ver = '{{ ver }}' group by time(1m)")

        return query

    def query_influx(self, value, scaling_method):
        """
        Retrieve the data from the influxdb database.

        Args:
            value (str): The value we wish the retrieve - either eru or qos.
            scaling_method (str): The scaling method for which we wish to
            retrieve the value.

        Returns:
            list(dir): A list of dictionaries representing influxdb
            observations.
        """
        client = self._get_client()
        version = "" if self._version == self.DEFAULT_VERSION else self._version

        full_query = Template(
            self._get_base_query(self._version)).render(value=value,
                                                        sm=scaling_method,
                                                        pt=self._pit,
                                                        tp=self._tp,
                                                        ver=version)

        res = client.query(full_query)
        return list(res.get_points())

    def fetch_data(self):
        """
        Query influxdb for the predictive and reactive data associated with the
        these pit and tp tags. Use jinja2 for rendering the queries.

        Returns:
            (dict, dict): dicts of the predictive and reactive data respectively,
            in the following form {"2016-4...": {"eru": .54, "qos": .321}},
            for 10s intervals.
        """

        store = {self.PREDICTIVE: None, self.REACTIVE: None}

        for scaling_method in store.keys():
            full_results = {}

            for value in self.POSSIBLE_VALUES:
                res = self.query_influx(value, scaling_method)

                for entry in res:
                    mean = entry["mean"]

                    if mean is not None:
                        timestamp = entry["time"]

                        if full_results.get(timestamp) is None:
                            full_results[timestamp] = {}
                        full_results[timestamp][value] = mean

            store[scaling_method] = full_results

        return (store[self.PREDICTIVE], store[self.REACTIVE])

    def _normalize(self, value, mean, std_dev):
        """
        Normalize the value given the mean and std_dev (take the z-score).

        Args:
            value (float): The value to be normalized (either an eru or qos).
            mean (float): The mean for normalization.
            std_dev (float): The std dev for normalization.

        Returns:
            float: The normalized value.
        """
        return (value - mean) / std_dev

    def eru_qos_sum(self, pred, react):
        """
        Process the predictive and reactive data sets so that for each previous
        observation is now a dict where the key is the time stamp and the value is
        the summation of eru and qos at that time.

        See the written thesis for a description of how eru and qos are summed.

        Args:
            pred (dict): A dict of the predictive auto-scaling observations,
                where the key is the time stamp and the value is a dict of eru and
                qos.
            react (dict): A dict of the reactive auto-scaling observations.

        Return:
            (dict, dict): A dict where the key is the timestamp and the value is the
            summation of eru and qos - first predictive and then reactive.
        """
        all_eru = [e["eru"] for e in pred.values()] + [e["eru"] for e in react.values()]
        all_qos = [e["qos"] for e in pred.values()] + [e["qos"] for e in react.values()]

        eru_mean, eru_std_dev = numpy.mean(all_eru), numpy.std(all_eru)
        qos_mean, qos_std_dev = numpy.mean(all_qos), numpy.std(all_qos)

        results = {}
        for scaling_method, data in {self.PREDICTIVE: pred, self.REACTIVE: react}.iteritems():
            for timestamp, entry in data.iteritems():
                eru, qos = entry["eru"], entry["qos"]
                n_eru = self._normalize(eru, eru_mean, eru_std_dev)
                n_qos = self._normalize(qos, qos_mean, qos_std_dev)

                # A hacky way to allow me to compare to trials just on the basis
                # of eru or qos as opposed to just their summation.
                if self._only_eru:
                    sum_eru_qos = -n_eru
                elif self._only_qos:
                    sum_eru_qos = -n_qos
                else:
                    sum_eru_qos = -n_eru + -n_qos

                data[timestamp] = sum_eru_qos

            results[scaling_method] = data

        return (results[self.PREDICTIVE], results[self.REACTIVE])

    def _get_version(self):
        """
        Return the version to be used when analysing.

        @TODO The version cli arg should always be specified. But the method of
        specifying which `version` to use is still kind of unstable. So we're
        just using a `getter` method to make any future changes more accessible.

        Return:
            str: The version.
        """

        return self._version

    def _get_file_name(self, file_type):
        """
        Return the file name for the graph.

        Args:
            file_type (str): Whether the file contains a graph or a json of
            summary statistics.

        Return:
            str: The title for the file name of the graph.
        """
        base_str = self.GRAPH if file_type == self.GRAPH else self.STATS

        qualifier = ""
        if self._only_eru:
            qualifier = "_only-eru"
        elif self._only_qos:
            qualifier = "_only-qos"

        file_name = "{0}/{1}_{2}_{3}_{4}{5}".format(self._output, base_str, self._pit,
                                                    self._tp, self._get_version(),
                                                    qualifier)
        return file_name

    def _get_y_axis(self):
        """
        Return the y axis title for the graphs.

        Return:
            str: The y-axis title for the graph, which changes depending on if
            its comparing ERU, QOS, or the sum.
        """
        if self._only_eru:
            return "ERU"
        elif self._only_qos:
            return "QOS"
        else:
            return "Summation of ERU and QOS"

    def _get_graph_title(self):
        """
        Return the title for the graph.

        Return:
            str: The title of the graph.
        """
        base_str = "Comparison of {0}"

        if self._only_eru:
            return base_str.format("ERU")
        elif self._only_qos:
            return base_str.format("QOS")
        else:
            return base_str.format("Summation of ERU and QOS")

    def _convert_time(self, date_str):
        """
        Convert a given date string to a datetime object.

        Args:
            date_str (str): The given date string.

        Results:
            datetime: A datetime object.
        """
        time_format = "%Y-%m-%dT%H:%M:%SZ"
        time = datetime.datetime.strptime(date_str, time_format)

        return time

    def convert_graph(self, pred, react):
        """
        Convert the data so that it is ready to be graphed.

        Args:
            pred (hash): The same as `react`, but predictive data.
            react (hash): A hash of timestamps where key is a timestamp and
            value is the summation of eru and qos, for reactive data.

        Returns:
            list, list, list: The x_vals (timestamps), predictive values, and
            reactive values.
        """
        # Cutoff any dangling values - fine to do because just 1rps tail.
        cutoff_length = min(len(pred.keys()), len(react.keys()))
        pred_timestamps = pred.keys()[:cutoff_length]
        react_timestamps = react.keys()[:cutoff_length]

        second_timestamps = [self._convert_time(t) for t in pred_timestamps]
        second_timestamps.sort()
        f_time = second_timestamps[0]

        x_vals = [(t - f_time).total_seconds() for t in second_timestamps]

        # @TODO Double check that this is sorting correctly. It should because
        # the formatting is YYYY-MM-DDTH-M-SZ.
        pred_timestamps.sort()
        react_timestamps.sort()

        results = {}
        for scaling_method, stamps_and_values in {self.PREDICTIVE:
                (pred_timestamps, pred), self.REACTIVE: (react_timestamps, react)}.iteritems():

            ordered_output = []
            (string_timestamps, dataset) = stamps_and_values

            # Sorting the string timestamps should still work.
            for time in string_timestamps:
                ordered_output.append(dataset.get(time))

            results[scaling_method] = ordered_output

        return x_vals, results[self.PREDICTIVE], results[self.REACTIVE]

    def graph(self, sum_p, sum_r):
        """
        Graph the predictive and reactive auto-scalings of eru and qos and output
        the graph to the output directory (with the appropriate label).

        Args:
            sum_p (dict): A dict where the key is the time stamp and value is
            the summation of eru and qos for predictive.
            sum_r (dict): Same as above but for reactive.
        """
        x_vals, pred_y_vals, react_y_vals = self.convert_graph(sum_p, sum_r)

        plot.plot(x_vals, pred_y_vals)
        plot.plot(x_vals, react_y_vals)
        plot.legend(["Predictive", "Reactive"], loc="upper left")

        plot.xlabel("Timestamp (s)")
        plot.ylabel(self._get_y_axis())
        plot.title(self._get_graph_title())

        plot.savefig(self._get_file_name(self.GRAPH))

    def calc_stats(self, pred_sums, react_sums):
        """
        Given an ordered list of pred_sums and react_sums, that correspond with
        each other, return the mean difference, std dev of difference, z_score,
        and p-value as part of the hash.

        Our null hypothesis is that mean difference between pred_sum[i] and
        react_sum[i] for all i is no different than 0.

        Because we do an upper tailed test, our alternative hypotehsis is that
        the mean difference between pred_sum[i] and react_sum[i] for all i is
        greater than 0.

        Args:
            pred_sums (list): An ordered list of the predictive sums of eru and
            qos.
            react_sums (list): An ordered list of the reactive sums of eru and
            qos.

        Returns:
            dict: A dict of statistical measures including "mean", "std_dev",
            "z_score", "p_score".
        """
        differences = []
        for i, _ in enumerate(pred_sums):
            pred_sum, react_sum = pred_sums[i], react_sums[i]
            diff = pred_sum - react_sum

            differences.append(diff)

        sample_mean = numpy.mean(differences)
        hyp_mean = 0
        std_dev = numpy.std(differences)

        z_score = (sample_mean - hyp_mean)  / std_dev

        # @TODO Is it ok to assume the distribution is normal?
        # @TODO Is this calculating what I think it is?
        p_value = 1 - scipy.stats.norm.cdf(z_score)

        ret_hash = {"mean": sample_mean,
                    "std_dev": std_dev,
                    "z_score": z_score,
                    "p_value": p_value}

        return ret_hash

    def _output_stats(self, stats):
        """
        Write the output stats to a file as json.

        Args:
            stats (dict): A dict of stats.
        """
        file_name = "{0}.json".format(self._get_file_name(self.STATS))

        with open(file_name, "w+") as json_file:
            json.dump(stats, json_file)

    def stats(self, sum_p, sum_r):
        """
        Output stats for the predictive and reactive auto-scalings of eru and qos and output
        to the output directory (with the appropriate label).

        Args:
            sum_p (dict): A dict where key is the time stamp and value is
            the summation of eru and qos for predictive.
            sum_r (dict): Same as above but for reactive.
        """

        # We assume that convert_graphs returns in order.
        _, pred_sums, react_sums = self.convert_graph(sum_p, sum_r)
        stats = self.calc_stats(pred_sums, react_sums)

        self._output_stats(stats)

    def run(self):
        """
        Retrieve the predictive and reactive data from InfluxDB, sums ero and
        qos, and the produces graph and summary statistics.
        """
        (predictive_data, reactive_data) = self.fetch_data()
        (sum_p, sum_r) = self.eru_qos_sum(predictive_data, reactive_data)

        self.graph(sum_p, sum_r)
        self.stats(sum_p, sum_r)

def parse_args():
    """
    Parse the arguments from the command line argument.

    @example
    - python evaluate.py PIT TP VERSION OUT [--only-eru] [--only-qos]
    - python evaluate.py 5s increase-decrease v2 output
    - python evaluate.py 135s increase-decrease v2 output --only-eru
    """
    parser = argparse.ArgumentParser(description="Process the evaluation test output.")

    parser.add_argument("pit", type=str, help="the pod initialization time (i.e. 5s)")
    parser.add_argument("tp", type=str, help="the traffic pattern (i.e. flash-crowd)")
    parser.add_argument("version", type=str, help="the version of trials")
    parser.add_argument("out", type=str, help="the directory to write to (i.e. output)")

    # @TODO Make this less hacky. But basically it allows us to specify if we
    # only want to compare eru or qos as opposed to their summation.
    parser.add_argument("--only-eru", action="store_true")
    parser.add_argument("--only-qos", action="store_true")

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()

    Evaluate(args.pit, args.tp, args.version, args.out, args.only_eru,
             args.only_qos).run()
