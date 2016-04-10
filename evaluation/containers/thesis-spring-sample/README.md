# thesis-spring-sample

### Determining pit

To determine how long it takes a pod containing a Spring web server, simply run
`gradle build buildDocker` and then run `docker run -p 8080:8080
mattjmcnaughton/thesis-spring-sample`, and Spring will print out how long it
takes the web server to initialize and be able to run requests.
