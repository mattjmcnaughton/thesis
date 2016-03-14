# TODO

A very high level list of tasks todo.

- [ ] Add docker-compose for running the test-server (using Gin) with a
  containerized influxDB and Grafana
  (https://github.com/kamon-io/docker-grafana-influxdb).
  - Update the Dockerfile as well.
- [ ] Add Makefile to automate all repeated tasks (testing,
  running godep, serving the app...) all tasks from the Makefile
  should be run in the Docker container using `godep`.
- [ ] Write the methods described in each file with accompanying tests.
- [ ] Write description of this test-server (particularly the HTTP endpoints),
  but also how it is run, and what it does, in the evaluation section of the
  thesis. Perhaps include small segments of the code as well.
- [ ] Determine how to configure the different versions of the container based
  on the scaling method being used (likely ENV variables).
- [ ] Deploy to Kubernetes for evaluation.
