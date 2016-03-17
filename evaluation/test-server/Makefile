# Makefile for automation.

# The name of the `test-server` image created by docker-compose.
COMPOSE_IMAGE = test-server_app

# The name of the `test-server` image within `docker-compose`.
COMPOSE_SERVICE = app

# The name of the image on docker hub (or Google container registry).
IMAGE_NAME = mattjmcnaughton/thesis-test-server

# A query for all the containers built through `docker-compose`.
DOCKER_QUERY = label=project=test-server

# A query for all relevant containers created through `docker-compose`.
CONTAINERS_QUERY := `docker ps -a -q -f $(DOCKER_QUERY)`

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
