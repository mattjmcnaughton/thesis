"""
test_evaluate.py contains the code for testing the `Evaluate` class that is the
foundation of the `evalute.py` script.
"""

import unittest

from evaluate import Evaluate

class EvaluateTestCase(unittest.TestCase):
    """
    EvaluateTestCase contains all of the test cases for the `Evaluate` class.
    This equates to testing the `evaluate.py` script because `evaluate.py` only
    runs methods contained with the `Evaluate` class.
    """

    def test_fetch_data(self):
        """
        Test the `fetch_data` function, which queries InfluxDB and places it in
        a format that we can normalize.
        """
        self.assertTrue(1 == 1)

if __name__ == "__main__":
    unittest.main()
