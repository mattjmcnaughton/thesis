# From https://spring.io/guides/gs/spring-boot-docker/

FROM frolvlad/alpine-oraclejdk8:slim
VOLUME /tmp
ADD thesis-spring-sample-0.1.0.jar app.jar
RUN sh -c 'touch /app.jar'
ENTRYPOINT ["java","-jar","/app.jar"]
