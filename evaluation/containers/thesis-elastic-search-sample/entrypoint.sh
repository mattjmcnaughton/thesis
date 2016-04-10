#!/bin/sh

# This script will run to initailize the Docker container. It simulates
# downloading a shard file, importing it into Elasticsearch, and then starting a
# web server.

wget https://www.elastic.co/guide/en/kibana/3.0/snippets/shakespeare.json
curl -XPUT elasticsearch:9200/_bulk --data-binary @shakespeare.json
python app.py
