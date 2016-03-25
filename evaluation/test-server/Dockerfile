# Dockerfile for `test-server`.

FROM golang:1.5

MAINTAINER mattjmcnaughton@gmail.com

# Set the Gopath env variables.
ENV GOPATH /go
ENV PATH /go/bin:$PATH

# Add go dependencies that are not bundled with Godeps.
RUN go get -u github.com/golang/lint/golint
RUN go get github.com/tools/godep
RUN go get -u github.com/codegangsta/gin

# Copy the local package files to the container (ignoring the files in
# `.dockerignore`).
ADD . /go/src/github.com/mattjmcnaughton/test-server

WORKDIR /go/src/github.com/mattjmcnaughton/test-server

# Download the dependencies
RUN godep restore

# Build the app.
RUN godep go install

# Expose the port on which we serve the app - we use 80 for production and 3000
# for development.
EXPOSE 80
EXPOSE 3000

# Run the app (when using docker-compose in dev mode, this will be overwritten
# by /go/bin/gin run main.go).
CMD /go/bin/test-server
