# Process

This directory contains everything I need to process the data from my evaluation
tests.

Essentially, it contains a python script called `evaluate.py` which takes
`pod-initialization-time` and `test-pattern` as arguments, as well as optional
flags for `--just-reactive` or `--just-predictive` and `--output`. It will
generate graphs of the summation of eru and qos for the appropriate data and
also will output the statistical significance of the difference of `sum_pred -
sum_react`.

Examples of how to run this command can be seen in the Makefile.
