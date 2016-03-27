# Makefile for commmon tasks.

TRAFFIC_GENERATOR_IMAGE = mattjmcnaughton/traffic-generator:latest

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

.DEFAULT_GOAL := push
