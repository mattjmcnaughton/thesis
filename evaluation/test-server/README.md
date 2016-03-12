# test-server

test-server is a containerizable Go web server used for testing different paradigms
of auto-scaling in Kubernetes. test-server is built to make it easy to configure
the different independent variables with respect to the server, most
specifically, how long it takes a pod containing the webserver to initialize.

## server.go

This file contains the simple HTTP Go server that we use for testing. This
server defines two endpoints.

- `/` is the HTTP endpoint to which our load generators will make requests. This
  endpoint will perform some CPU intensive task (so that we actually use up
  enough CPU to encourage auto-scaling) and then write the current cpu
  utilization percentage and some metric of quality of service to an InfluxDB
  database. This write to the database will contain an indication of how the pod
  is being auto-scaled (i.e. static, reactive, predictive), and this indication
  will also be configured in `ENV`.
- `/ready` is the HTTP endpoint used for the Kubernetes `ReadinessProbe`. This
  endpoint will wait an amount of seconds configured in `ENV` and then return
  200. This enables easy experimentation with different pod initialization
  times.

## yaml

The `yaml` directory contains the different configuration files for the pods,
replication controllers, services, and horizontal auto-scalers needed for
testing.
