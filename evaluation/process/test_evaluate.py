"""
test_evaluate.py contains the code for testing the `Evaluate` class that is the
foundation of the `evalute.py` script.
"""

import os
import tempfile
import unittest

from mock import MagicMock

from evaluate import Evaluate

class InfluxDBMock(object):
    """
    A class providing methods for mocking the influxdb database.
    """

    # Class wide constants.
    ERU = "eru"
    QOS = "qos"
    REACTIVE = "reactive"
    PREDICTIVE = "predictive"

    # Constants to have a single look up for values we'll test for.
    FIRST_TIMESTAMP = "2016-04-13T23:50:00Z"
    FIRST_REACT_ERU = 2.0
    FIRST_REACT_QOS = 3.0

    @staticmethod
    def query_influx(value, scaling_method):
        """
        A static method that takes as input a value and a scaling method and
        returns stubbed output.

        Args:
            value (str): The value we want (either ERU or QOS)
            scaling_method(str): The scaling method we want (reactive or
            predictive).

        Return:
            list(dict): A list of points.
        """

        # Make predictive more than reactive so I can test that they are aligned
        # correctly by checking that pred_sum[i] < reactive_sum[i]
        if value == InfluxDBMock.ERU:
            if scaling_method == InfluxDBMock.REACTIVE:
                return [{"mean": InfluxDBMock.FIRST_REACT_ERU,
                         "time": InfluxDBMock.FIRST_TIMESTAMP},
                        {"mean": 5.0, "time": "2016-04-13T23:51:00Z"},
                        {"mean": None, "time": "2016-04-13T23:52:00Z"}]
            elif scaling_method == InfluxDBMock.PREDICTIVE:
                return [{"mean": 1.0, "time": InfluxDBMock.FIRST_TIMESTAMP},
                        {"mean": 4.0, "time": "2016-04-13T23:51:00Z"}]
        elif value == InfluxDBMock.QOS:
            if scaling_method == InfluxDBMock.REACTIVE:
                return [{"mean": InfluxDBMock.FIRST_REACT_QOS,
                         "time": InfluxDBMock.FIRST_TIMESTAMP},
                        {"mean": 7.0, "time": "2016-04-13T23:51:00Z"}]
            elif scaling_method == InfluxDBMock.PREDICTIVE:
                return [{"mean": 1.0, "time": InfluxDBMock.FIRST_TIMESTAMP},
                        {"mean": 6.0, "time": "2016-04-13T23:51:00Z"}]

class EvaluateTestCase(unittest.TestCase):
    """
    EvaluateTestCase contains all of the test cases for the `Evaluate` class.
    This equates to testing the `evaluate.py` script because `evaluate.py` only
    runs methods contained with the `Evaluate` class.
    """

    # PIT, TP, VERSION are the pod initialization time, test pattern, and
    # version that we mock for.
    PIT = "5s"
    TP = "increase-decrease"
    VERSION = "v2"

    def __init__(self, *args, **kwargs):
        super(EvaluateTestCase, self).__init__(*args, **kwargs)
        self._tmp_output = None

    def test_fetch_data(self):
        """
        Test the `fetch_data` function, which queries InfluxDB and places it in
        a format that we can normalize.

        We test that react and pred return the same number of keys.

        Additionally, we test that each entry is in the correct format (i.e.
        combined eru and qos).
        """
        evaluate = self._mock_evaluate()
        (pred, react) = evaluate.fetch_data()

        # Assert we have the same number of observations for react and pred.
        self.assertEqual(react.keys(), pred.keys())

        # Assert all observations are in the correct format.
        for dataset in [react, pred]:
            for entry in dataset.values():
                self.assertIsNotNone(entry.get(InfluxDBMock.QOS))
                self.assertIsNotNone(entry.get(InfluxDBMock.ERU))

        # Assert that entries correspond.
        self.assertEqual(react[InfluxDBMock.FIRST_TIMESTAMP][InfluxDBMock.ERU],
                         InfluxDBMock.FIRST_REACT_ERU)
        self.assertEqual(react[InfluxDBMock.FIRST_TIMESTAMP][InfluxDBMock.QOS],
                         InfluxDBMock.FIRST_REACT_QOS)


    def test_eru_qos_sum(self):
        """
        Test the `eru_qos_sum` method, which processes the predictive and
        reactive data set to sum eru and qos.
        """
        evaluate = self._mock_evaluate()
        (tmp_p, tmp_r) = evaluate.fetch_data()
        (pred, react) = evaluate.eru_qos_sum(tmp_p, tmp_r)

        # Assert that we have the same number of observations for react and
        # pred.
        self.assertEqual(react.keys(), pred.keys())

        # Ensure that every observation has a qos value.
        for dataset in [react, pred]:
            # Values in the datasets are all erus.
            for entry in dataset.values():
                self.assertIsNotNone(entry)

        # @TODO How to test what values to expect...

    def test_convert_graph(self):
        """
        Test that converting the data to a format outputible through the graph
        works. This basically means that we have an ordered list of normalized
        timestamps in seconds, and that we have an ordered list of predictive
        and reactive summations of eru and qos that are the same length.
        """
        evaluate = self._mock_evaluate()
        (tmp_p, tmp_r) = evaluate.fetch_data()
        (tmp_p, tmp_r) = evaluate.eru_qos_sum(tmp_p, tmp_r)
        (x_vals, pred, react) = evaluate.convert_graph(tmp_p, tmp_r)

        # Test the xvals start at 0 and are in order.
        self.assertEqual(x_vals[0], 0)
        self.assertTrue(sorted(x_vals))

        # Check that there are the same number of pred and react values.
        self.assertEqual(len(pred), len(react))

        # Check that pred and react are aligned properly by checking that pred
        # is always > than react (becuase it has smaller initial eru and qos
        # values - where small represents good eru and qos).
        for i, _ in enumerate(pred):
            self.assertTrue(pred[i] > react[i])

    def test_graph(self):
        """
        Test creating the graphs. It may actually make more sense to test the
        functions that generate the input for this graph in addition to testing
        the output graphs, although that would possibly require me to make some
        previously private methods public.
        """
        evaluate = self._mock_evaluate()
        (tmp_p, tmp_r) = evaluate.fetch_data()
        (sum_p, sum_r) = evaluate.eru_qos_sum(tmp_p, tmp_r)

        evaluate.graph(sum_p, sum_r)

        has_file = self._file_exists_in_dir(Evaluate.GRAPH, self._get_tmp_dir())
        self.assertTrue(has_file)

    def test_calc_stats(self):
        """
        Test the calculate stats function is working correctly and returning the
        values we expect.
        """
        evaluate = self._mock_evaluate()
        (tmp_p, tmp_r) = evaluate.fetch_data()
        (sum_p, sum_r) = evaluate.eru_qos_sum(tmp_p, tmp_r)
        (_, pred_y_vals, react_y_vals) = evaluate.convert_graph(sum_p, sum_r)

        stats = evaluate.calc_stats(pred_y_vals, react_y_vals)

        # Assert that the mean, std_dev, z_score, and p_score are all greater
        # than 0, which they should be because all of our original predictive
        # values are less than the reactive values, meaning that their sum or
        # eru and qos should be greater.
        for val in stats.values():
            self.assertTrue(val > 0)

    def test_stats(self):
        """
        Test generating the stats. It is a similar situation to `test_graph` in
        which it may make more sense to test the actual calculation of the
        stats, as that is what I'm most interested in. We can also test that the
        file is created and named correctly.
        """
        evaluate = self._mock_evaluate()
        (tmp_p, tmp_r) = evaluate.fetch_data()
        (sum_p, sum_r) = evaluate.eru_qos_sum(tmp_p, tmp_r)

        evaluate.stats(sum_p, sum_r)

        has_file = self._file_exists_in_dir(Evaluate.STATS, self._get_tmp_dir())
        self.assertTrue(has_file)

    def test_run(self):
        """
        Test that run executes without crashing.
        """
        evaluate = self._mock_evaluate()
        evaluate.run()

    def _file_exists_in_dir(self, file_substr, directory):
        """
        Test that running the entire evaluate process does not crash.

        Args:
            file_substr (str): The name of a substr we desire to find in the
            file.
            directory (str): The name of the directory.

        Return:
            bool: A boolean indicating whether the file was found.
        """
        # Check that the file exists.
        for poss_file in os.listdir(directory):
            file_path = os.path.join(directory, poss_file)
            if os.path.isfile(file_path) and file_substr in poss_file:
                return True

        return False

    def _get_tmp_dir(self):
        """
        Return a temporary output dir in which we can write files.

        Returns:
            (str): The absolute path of the new directory.
        """
        if self._tmp_output is None:
            self._tmp_output = tempfile.mkdtemp()

        return self._tmp_output

    def _mock_evaluate(self):
        """
        Create a mock `Evaluate` class, with all methods that access the
        influxdb database stubbed out.

        Returns:
            Evaluate: An instance of the Evaluate class.
        """
        evaluate = Evaluate(self.PIT, self.TP, self.VERSION, self._get_tmp_dir())

        evaluate.query_influx = MagicMock()
        evaluate.query_influx = InfluxDBMock.query_influx

        return evaluate

if __name__ == "__main__":
    unittest.main()
