# Makefile for commmon tasks.

TRAFFIC_GENERATOR_IMAGE = mattjmcnaughton/traffic-generator:latest

# The path for k8s configuration files.
CONFIG_PATH = config/generated

# `$ make generate_k8s_config`
#
# Update the configuration files for running the traffic-generator on
# Kubernetes. Because this is a much simpler use case than `traffic-server`, we
# can just use jinja2-cli.
generate_k8s_config:
	docker run --rm -i -v $(shell pwd):/code mattjmcnaughton/thesis-python:latest python /code/config/generate_k8s_config.py

# `$ make build`
#
# Build the `traffic-generator` image.
build:
	docker build -t $(TRAFFIC_GENERATOR_IMAGE) .

# `$ make push`
#
# Push the `traffic-generator` image to the Dockerfile.
push: build
	docker push $(TRAFFIC_GENERATOR_IMAGE)

# Start all kubernetes objects needed for testing with the `traffic-generator`.
# It is necessary to specify the test plan rc config file with
# `TG_RC`.
start_k8s_objects:
	kubectl create -f $(CONFIG_PATH)/$(TG_RC)

# `make test_start`
#
# This command starts all parts of the k8s tests that rely upon `test_start`. It
# also ensures that the latest containers and configuration files are being
# used.
#
# @TODO See `start_k8s_objects` for a list of environment variables that must be
# set.
test_start: build push generate_k8s_config start_k8s_objects

# Stop all traffic-generator rcs running on k8s.
stop_k8s_objects:
	kubectl delete -f $(CONFIG_PATH)

# `make test_stop`
#
# This function is responsible for stopping all parts of the k8s tests that rely
# upon `test_stop`.
test_stop: stop_k8s_objects

.DEFAULT_GOAL := push
