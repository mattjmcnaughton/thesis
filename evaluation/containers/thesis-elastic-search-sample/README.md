# thesis-elastic-search-sample

### Estimating pod initialization time

To estimate pod initialization time, first run `docker-compose stop
[elasticsearch|web]` and `docker-compose rm [elasticsearch|web]` to ensure that
we are starting with fresh containers. Then time how long it takes
`docker-compose up` to get to the Flask app running. First it will have to
download a 25.2MB data file over the network and load it into an elastic search
database.
