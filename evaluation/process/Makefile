# Makefile for processing the results of the evaluation tests.

# `$ make test`
#
# Test the `Evaluation` class that serves as the formation of the `evaluation.py` script.
# We do not need to include the `.env` file for connecting to the database,
# because we are stubbing out the method that connects to the database.
test:
	docker run --rm -i mattjmcnaughton/thesis-python:latest python /code/test_evaluate.py

# `$ make process`
#
# Process the results of an evaluation test and output the results into the
# `output` dir. The pod intitialization time is specified by $PIT and the traffic
# pattern is specified by $TP. The output dir to write to is specified by $OUT.
#
# @example `export PIT=5s; export TP=increase-decrease; export OUT=/code/output; make
# process`.
process:
	docker run --rm --env_file=.env -i -v $(shell pwd):/code mattjmcnaughton/thesis-python:latest python /code/evaluate.py $(PIT) $(TP) $(OUT)
