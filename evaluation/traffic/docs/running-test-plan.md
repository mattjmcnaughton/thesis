# Running Test Plans

This document describes how to run a `test-plan` on Kubernetes.

## Generating configuration files

The `generate_k8s_config.py` script will automatically generate a k8s
replication controller configuration file for any test plan that we have
created.

## Running test plan

Running the test plan is as simple as creating the proper replication controller
on Kubernetes, using `kubectl create -f
traffic-generator-controller-TEST_PLAN.yaml`. The test plan will start running
automatically. Because it will immediately start sending requests to the
service, this should only be done when the `test-server` service is already
running.
