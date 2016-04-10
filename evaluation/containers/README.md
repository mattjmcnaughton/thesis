# Containers

This directory contains Dockerfiles for common containers that I need throughout
the course of this thesis. Containers are placed in this directory if they are
not substantial enough to be associated with a single directory (i.e. the
configuration for the custom container for Apache JMeter is in the `traffic`
directory.)

## Container List

- thesis-python: This container is a python development environment containing
  all of the dependencies that I need (i.e. jinja, influxdb, numpy...)
- thesis-go-sample: This container helps us measure the response time of a web
  server with a lightweight initialization process.
- thesis-spring-sample: This container helps us measure the response time of a
  web server with a more heavy duty initialization process.
- thesis-elastic-search-sample: This container wraps an application that must
  download data and load it into elastic search before it can start serving web
  requests. This is intended to symbolize an application that must download
  shard files.
