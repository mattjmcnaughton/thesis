# A universal Makefile for evaluation. This Makefile contains only two commands,
# `test_start` and `test_stop` which automate the process for running an entire
# test sequence and then also tearing that sequence down.

# `make test_start`
#
# Start running a test sequence, by running `make test_start` in the `test-server`
# and `traffic`directories. A couple of environment variables must be set, as
# can be seen in the example below.
#
# @EXAMPLE: export TS_RC=test-server-controller-reactive-5s-v1.yaml; export TG_RC=traffic-generator-controller-increase-decrease-test-plan.yaml; export HPA=TRUE; export PREDICTIVE=TRUE; make test_start
# @TODO Be sure to set HPA/PREDICTIVE to FALSE if we don't want to use them,
# because otherwise the values will carry over.
test_start:
	cd test-server && make $@
	cd traffic && make $@

# `make test_stop`
#
# Similar to `test_start`, but for stopping a test and tearing down any
# aftermath from the test.
#
# We include the `-` to ignore errors, because there will be errors when we try
# to stop configuration files that don't exist.
test_stop:
	-cd traffic && make $@
	-cd test-server && make $@
