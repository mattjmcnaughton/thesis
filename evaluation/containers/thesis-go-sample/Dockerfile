# Dockerfile to run the simplest possible GO http app.
#
# See `test-server` for documentation of what each function does.

FROM golang:1.5

MAINTAINER mattjmcnaughton@gmail.com

ENV GOPATH /go
ENV PATH /go/bin:$PATH

ADD . /go/src/github.com/mattjmcnaughton/thesis-go-sample
WORKDIR /go/src/github.com/mattjmcnaughton/thesis-go-sample

RUN go install

EXPOSE 80
EXPOSE 3000

CMD /go/bin/thesis-go-sample
