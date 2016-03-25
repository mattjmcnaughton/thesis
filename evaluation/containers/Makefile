# Makefile for building and pushing Docker images.

# The image containing a python environment usable throughout this thesis.
THESIS_PYTHON_IMAGE = mattjmcnaughton/thesis-python:latest

# Build the `thesis-python` image.
build_thesis_python:
	docker build -t $(THESIS_PYTHON_IMAGE) thesis-python

# `make push_thesis_python`
#
# Push the `thesis-python` image to Docker hub.
push_thesis_python: build_thesis_python
	docker push $(THESIS_PYTHON_IMAGE)

# `make all`
#
# Push all images to Docker hub.
push_all: push_thesis_python

# If no option is specified, then build and push all images.
.DEFAULT_GOAL := push_all
