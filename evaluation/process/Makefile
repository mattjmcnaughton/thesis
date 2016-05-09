# Makefile for processing the results of the evaluation tests.

# `$ make test`
#
# Test the `Evaluation` class that serves as the formation of the `evaluation.py` script.
# We do not need to include the `.env` file for connecting to the database,
# because we are stubbing out the method that connects to the database.
test:
	docker run --rm -i -v $(shell pwd):/code mattjmcnaughton/thesis-python:latest python /code/test_evaluate.py

# `$ make process`
#
# Process the results of an evaluation test and output the results into the
# `output` dir. The pod intitialization time is specified by $PIT and the traffic
# pattern is specified by $TP. The output dir to write to is specified by $OUT.
# The version, [v1|v2...], is specified by `VERSION`.
#
# @TODO `VERSION` must be specified.
#
# @example `export PIT=5s; export TP=increase-decrease; export VERSION=v2; export OUT=/code/output; make process`.
process:
	docker run --rm --env-file=.env -i -v $(shell pwd):/code mattjmcnaughton/thesis-python:latest python /code/evaluate.py $(PIT) $(TP) $(VERSION) $(OUT)

# `make backup`
#
# Backup the data stored into the influxdb database into the `backup/`
# directory.
#
# @Example `export HOST=https://enchantmentunderthesea-hoverboard-44.c.influxdb:8086; export USERNAME=username; export PASSWORD=password; export DATABASE=test-server-prod; export OUTPUT=output/backup; make backup`
backup:
	curl -G $(HOST)/query -u $(USERNAME):$(PASSWORD) --data-urlencode "db=$(DATABASE)" --data-urlencode "q=SELECT * FROM METRICS" > $(OUTPUT)
