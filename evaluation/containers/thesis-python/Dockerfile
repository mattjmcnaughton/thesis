# Dockerfile for `thesis-python`.
#
# This Dockerfile contains a development environment for doing all of the
# necessary python work.

FROM python:2.7

MAINTAINER mattjmcnaughton@gmail.com

RUN apt-get update  -y
RUN apt-get install -y python-numpy python-scipy python-matplotlib ipython ipython-notebook python-pandas python-sympy python-nose

ADD . /config

WORKDIR /config

RUN pip install -r requirements.txt
