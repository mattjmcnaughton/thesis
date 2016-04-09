# Makefile for automation.

# The name of the `test-server` image created by docker-compose.
COMPOSE_IMAGE = test-server_app

# The name of the `test-server` image within `docker-compose`.
COMPOSE_SERVICE = app

# The name of the image on docker hub.
IMAGE_NAME = mattjmcnaughton/test-server
IMAGE_NAME_WITH_VERSION = $(IMAGE_NAME):`git rev-parse HEAD`

# A query for all the containers built through `docker-compose`.
DOCKER_QUERY = label=project=test-server

# A query for all relevant containers created through `docker-compose`.
CONTAINERS_QUERY := `docker ps -a -q -f $(DOCKER_QUERY)`

# The path in which k8s configuration files live.
CONFIG_PATH = config/generated

# Force docker-compose to rebuild the image.
# This only needs to be run after updating the Dockerfile.
#
# @TODO Is this necessary?
force_compose_build:
	docker-compose build $(COMPOSE_SERVICE)

# `make lint`
#
# Run the go linter on all Go code.
lint:
	docker-compose run $(COMPOSE_SERVICE) golint ./...

# `make test`
#
# Run all of the go tests.
test:
	docker-compose run $(COMPOSE_SERVICE) godep go test -v ./...

# `make check`
#
# Check the style and correctness of the code.
check: lint test

# `make run`
#
# Run the application.
run:
	docker-compose up $(COMPOSE_SERVICE)

# `make stop`
#
# Stop all running containers.
stop:
	docker stop $(CONTAINERS_QUERY)

# `make clean`
#
# Clean up old Docker images and containers.
clean: stop
	docker rm $(CONTAINERS_QUERY) && \
	docker rmi $(IMAGE_NAME)

# `make save_godep`
#
# Update the go dependencies.
# @TODO This is def. not the best way, try to fix later.
save_godep:
	echo "Navigate to test-server in $$GOROOT and do manually on local machine for now."

# `make restore_godep`
#
# Restore the go dependencies.
restore_godep:
	docker-compose run $(COMPOSE_SERVICE) godep restore

# `make build`
#
# Build the `mattjmcnaughton/test-server` image, with the latest version tagged
# as the git commit.
build:
	docker build -t $(IMAGE_NAME_WITH_VERSION) .

# `make push`
#
# Push the latest image of the `mattjmcnaughton/test-server`, tagged with the
# git commit, to Docker Hub.
push: build
	docker push $(IMAGE_NAME_WITH_VERSION)

# `make generate_k8s_config`
#
# Update the Kubernetes configuration files, found in `/config`, so the
# different configuration files for pods/replication
# controllers/services/auto-scalingers reflect the different options for scaling
# methods, container versions, and pod initialization time.
#
# @TODO Currently we need to run `git rev-parse HEAD` on the local machine, not
# the Docker container, and then pass it as an argument to the program. The
# calculation on the local host is necessary because we are not confident the
# Docker container will have either Git nor access to the `.git` directory.
generate_k8s_config:
	docker run --rm -i -v $(shell pwd)/config:/config mattjmcnaughton/thesis-python:latest python /config/generate_k8s_config.py $(shell git rev-parse HEAD)

# Start all kubernetes objects needed for testing. It is necessary to specify
# `TS_RC` as an environment file, as well as `HPA=TRUE` as
# an environment variable if we wish to create a reactive auto-scaler.
#
# @TODO Is it possible to not use environment variables?
# @TODO We will need a way of specifying if we are using predictive or reactive
# auto-scaling.
start_k8s_objects:
	kubectl create -f $(CONFIG_PATH)/$(TS_RC) &&
	kubectl create -f $(CONFIG_PATH)/test-server-service.yaml &&
	ifeq ($(HPA), "TRUE")
		kubectl create -f $(CONFIG_PATH)/hpa-test-server.yaml
	endif

# `make test_start`
#
# This command is responsible for running all parts of the k8s test that rely
# upon `test-server`. It also includes ensures that the latest containers and
# configuration files are being used.
#
# @TODO See `start_k8s_object` for a list of environment variables that must be
# set.
test_start: build push generate_k8s_config start_k8s_objects

# Stop all rcs, svcs, and hpas running on k8s.
stop_k8s_objects:
	kubectl delete -f $(CONFIG_PATH)

# `make test_stop`
#
# This function is responsible for stopping all parts of the k8s tests that rely
# upon `test-server`.
test_stop: stop_k8s_objects
