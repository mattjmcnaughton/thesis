# Dockerfile for `test-server`.

FROM golang:1.5

MAINTAINER mattjmcnaughton@gmail.com

# Set the Gopath env variables.
ENV GOPATH /go
ENV PATH /go/bin:$PATH

# Add go dependencies that are not bundled with Godeps.
RUN go get -u github.com/golang/lint/golint
RUN go get -u github.com/tools/godep

# Copy the local package files to the container (ignoring the files in
# `.dockerignore`).
ADD . /go/src/github.com/mattjmcnaughton/test-server

WORKDIR /go/src/github.com/mattjmcnaughton/test-server

# Download the dependencies
RUN godep restore

# Build the app.
RUN go install

# Expose the port on which we serve the app.
EXPOSE 8080

# Run the app.
CMD /go/bin/test-server
