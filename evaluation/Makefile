# A universal Makefile for evaluation. This Makefile contains only two commands,
# `test_start` and `test_stop` which automate the process for running an entire
# test sequence and then also tearing that sequence down.

# `make test_start`
#
# Start running a test sequence, by running `make test_start` in the `test-server`
# and `traffic`directories. A couple of environment variables must be set, as
# can be seen in the example below.
#
# @EXAMPLE: TS_RC= test-server-controller-reactive-5s.yaml; TG_RC=traffic-generator-controller-increase-decrease-test-plan.yaml; HPA=TRUE; make test_start
test_start:
	cd test-server && $(MAKE) $@ &&
	cd ../traffic && $(MAKE) $@

# `make test_stop`
#
# Similar to `test_start`, but for stopping a test and tearing down any
# aftermath from the test.
test_stop:
	cd traffic && $(MAKE) $@ &&
	cd ../test-server && $(MAKE) $@