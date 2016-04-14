"""
evaluation.py contains code for donwloading data from the InfluxDB database
instance, processing it to get graphs and statistical measures comparing the
difference for the summation of eru and qos for predictive vs reactive. It then
outputs the graphs and statistical measurements to the specified output
directory.
"""

import argparse
import os

import numpy

from influxdb import InfluxDBClient
from jinja2 import Template

def parse_args():
    """
    Parse the arguments from the command line argument.

    @example
    - python evaluate.py PIT TP OUT
    - python evaluate.py 5s increase-decrease output
    """
    parser = argparse.ArgumentParser(description="Process the evaluation test output.")

    parser.add_argument("pit", type=str, help="the pod initialization time (i.e. 5s)")
    parser.add_argument("tp", type=str, help="the traffic pattern (i.e. flash-crowd)")
    parser.add_argument("out", type=str, help="the directory to which to write about (i.e. output)")

    return parser.parse_args()

def fetch_data(pit, tp):
    """
    Query influxdb for the predictive and reactive data associated with the
    these pit and tp tags. Use jinja2 for rendering the queries.

    @TODO Factor this single method into many smaller methods.

    Args:
        pit (str): The pod initialization time tag.
        tp (str): The traffic pattern tag.

    Returns:
        (dict, dict): dicts of the predictive and reactive data respectively,
        in the following form {"2016-4...": {"eru": .54, "qos": .321}},
        for 10s intervals.
    """
    client = InfluxDBClient(host=os.environ["DATABASE_HOST"],
                            port=os.environ["DATABASE_PORT"],
                            username=os.environ["DATABASE_USER"],
                            password=os.environ["DATABASE_PASSWORD"],
                            database=os.environ["DATABASE_NAME"],
                            ssl=True)

    # @TODO Right now this assumes tests were run in the last 10d, which sames
    # like a fairly safe assumption, but is an assumption all the same.
    # @TODO Currently we group by 10s measurements, is that what we want?
    query = ("SELECT MEAN({{ value }}) from METRICS where time > now() - 10d and "
             "sm = '{{ sm }}' and pit = '{{ pt }}' and tp = '{{ tp }}'"
             "group by time(10s)")

    base_query = Template(query).render(pit=pit, tp=tp)

    store = {"predictive":  None, "reactive": None}
    for scaling_method in store.keys():
        scaling_query = Template(base_query).render(sm=scaling_method)

        full_results = {}
        for value in ["eru", "qos"]:
            full_query = Template(scaling_query).render(value=value)
            res = client.query(full_query)

            for entry in res.get_points():
                if entry["mean"] is not None:
                    timestamp = entry["time"]
                    if full_results.get(timestamp) is None:
                        full_results[timestamp] = {}
                    full_results[timestamp][value] = entry["mean"]

        store[scaling_method] = full_results

    return (store["predictive"], store["reactive"])

def eru_qos_sum(predictive, reactive):
    """
    Process the predictive and reactive data sets so that for each previous
    observation is now a dict where the key is the time stamp and the value is
    the summation of eru and qos at that time.

    See the written thesis for a description of how eru and qos are summed.

    Args:
        predictive (dict): A dict of the predictive auto-scaling observations,
            where the key is the time stamp and the value is a dict of eru and
            qos.
        reactive (dict): A dict of the reactive auto-scaling observations.

    Return:
        (dict, dict): A dict where the key is the timestamp and the value is the
        summation of eru and qos.
    """
    all_eru = [entry["eru"] for entry in predictive.values()] + [entry["eru"]
            for entry in reactive.values()]
    all_qos = [entry["qos"] for entry in predictive.values()] + [entry["qos"]
            for entry in reactive.values()]

    eru_mean, eru_std_dev = numpy.mean(all_eru), numpy.std(all_eru)
    qos_mean, qos_std_dev = numpy.mean(all_qos), numpy.std(all_qos)

    results = {}
    for scaling_method, data in {"predictive": predictive, "reactive":
            reactive}.iteritems():
        for timestamp, entry in data.iteritems():
            eru, qos = entry["eru"], entry["qos"]
            n_eru = (eru - eru_mean) / eru_std_dev
            n_qos = (qos - qos_mean) / qos_std_dev

            sum_eru_qos = -n_eru + -n_qos
            data[timestamp] = sum_eru_qos

        results[scaling_method] = data

    return (results["predictive"], results["reactive"])

def graph(sum_p, sum_r, output):
    """
    Graph the predictive and reactive auto-scalings of eru and qos and output
    the graph to the output directory (with the appropriate label).

    Args:
        sum_p (dict): A dict where the key is the time stamp and value is
        the summation of eru and qos for predictive.
        sum_r (dict): Same as above but for reactive.
        output (string): The directory in which to place the graphs.
    """
    pass

def stats(sum_p, sum_r, output):
    """
    Output stats for the predictive and reactive auto-scalings of eru and qos and output
    to the output directory (with the appropriate label).

    Args:
        sum_p (dict): A dict where key is the time stamp and value is
        the summation of eru and qos for predictive.
        sum_r (dict): Same as above but for reactive.
        output (string): The directory in which to place the output json.
    """
    pass


def process(pit, tp, output):
    """
    Process the test results comparing reactive and predictive auto-scaling for
    this combination of pod initialization time and traffic-pattern, and write
    the resulting graph and json describing the stastical measurements to
    labelled files in the output dir.

    Args:
        pit (str): The pod initialization time tag.
        tp (str); The traffic pattern tag.
        output (str): The directory to write the output.
    """

    # Fetch the data in 10s aggregated chunks.
    (predictive_data, reactive_data) = fetch_data(pit, tp)

    # Get the summation of eru and qos for each measure for both data sets.
    (sum_p, sum_r) = eru_qos_sum(predictive_data, reactive_data)

    # Output graphs of the normalized data.
    graph(sum_p, sum_r, output)
    stats(sum_p, sum_r, output)

if __name__ == "__main__":
    args = parse_args()
    process(args.pit, args.tp, args.out)
