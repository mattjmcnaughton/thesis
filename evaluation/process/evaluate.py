"""
evaluation.py contains code for donwloading data from the InfluxDB database
instance, processing it to get graphs and statistical measures comparing the
difference for the summation of eru and qos for predictive vs reactive. It then
outputs the graphs and statistical measurements to the specified output
directory.
"""

import argparse
import yaml

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
    these pit and tp tags.

    Args:
        pit (str): The pod initialization time tag.
        tp (str): The traffic pattern tag.

    Returns:
        (list, list): Lists of the predictive and reactive data respectively.
    """
    return ([], [])

def eru_qos_sum(predictive, reactive):
    """
    Process the predictive and reactive data sets so that for each previous
    observation is now a hash where the key is the time stamp and the value is
    the summation of eru and qos at that time.

    Args:
        predictive (list): A list of the predictive auto-scaling observations.
        reactive (list): A list of the reactive auto-scaling observations.

    Return:
        (list, list): Lists of the summation of eru and qos for predictive and
        reactive respectively.
    """
    return ([], [])

def graph(sum_p, sum_r, output):
    """
    Graph the predictive and reactive auto-scalings of eru and qos and output
    the graph to the output directory (with the appropriate label).

    Args:
        sum_p (list): A list of hashs where key is the time stamp and value is
        the summation of eru and qos for predictive.
        sum_r (list): Same as above but for reactive.
        output (string): The directory in which to place the graphs.
    """
    pass

def stats(sum_p, sum_r, output):
    """
    Output stats for the predictive and reactive auto-scalings of eru and qos and output
    to the output directory (with the appropriate label).

    Args:
        sum_p (list): A list of hashs where key is the time stamp and value is
        the summation of eru and qos for predictive.
        sum_r (list): Same as above but for reactive.
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
