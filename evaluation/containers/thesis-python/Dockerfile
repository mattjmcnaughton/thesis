# Dockerfile for `thesis-python`.
#
# This Dockerfile contains a development environment for doing all of the
# necessary python work.

FROM python:2.7

MAINTAINER mattjmcnaughton@gmail.com

ADD . /config

WORKDIR /config

RUN pip install -r requirements.txt
