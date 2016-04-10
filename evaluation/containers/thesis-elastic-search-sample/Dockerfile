# Contains a elasticsearch/python application that first downloads a shard data
# file and loads it into elasticsearch, and then runs a python web app.

FROM ubuntu:latest
MAINTAINER mattjmcnaughton@gmail.com

RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential wget curl

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt
RUN chmod 700 ./entrypoint.sh

CMD ["sh", "/app/entrypoint.sh"]
