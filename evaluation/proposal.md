# Evaluation Proposal

## What do we want to evaluate?

We want to see if we have accomplished the specific goal of this thesis: to
increase the summation of efficient resource utilization (ERU) and quality of
service (QOS) in Kubernetes.

## How will we know if we accomplished this goal (in general)?

We will compare the summation of ERU and QOS for average/max static provisioning
reactive auto-scaling, and predictive auto-scaling.

## How do we measure the necessary metrics?

#### ERU

We will measure ERU as the amount of CPU allocated to the replica pods.

#### QOS

We will measure QOS as request response time. In other words, all of the running
pods will be behind a service and will receive the same HTTP request, which they
most process (ideally this will require some CPU) and respond to.

#### Recording Metrics

It seems like the best option is to have some way of calculating the efficient
resource utilization and quality of service metric within each container. So
efficient resource utilization could be dividing the amount of CPU the
application is using by the amount the container has reserved. And quality of
service could be timing how long it takes to do some standardized calculation.
And then these values can be written directly to a database from the container
(instead of trying to return them as part of the HTTP request and then somehow
aggregate them all together). Each entry into the database could be tagged with
where it came from, so we know if its is from static, reactive, or predictive...
I'm thinking influxDB makes a lot of sense as the
database, as its built for time series data, and it also looks like it would be
fairly easy to set up graphing with Grafana on top.

## Constructing test environment

#### Containers

Our containers will have to be sure to define some sort of readiness probe (as
this is vital to the whole concept of predictive auto-scaling). It probably
makes the most sense to define a HTTP readiness probe, the process for which is
outlined [here](http://kubernetes.io/docs/user-guide/production-pods/#liveness-and-readiness-probes-aka-health-checks).

We will also need to define different types of containers, with different
initialization times.

## What independent variables will we examine?

#### All

- Traffic request pattern
- Pod initialization time
- Size of cluster

#### Predictive auto-scaling specific

- Method of predicting future resource utilization
- Threshold levels

## What dependent variables will we examine?

We will examine the summation of ERU and QOS - we need to be sure to have some
way of balancing the two such that they have equal impact. We will examine the
impact of certain individual independent variables on ERU and QOS individually.

## Anything else we're interested in?

In what scenarios is it most important to have predictive auto-scaling enabled.
In what scenarios does predictive auto-scaling have little impact.

## What are other metrics of interest?

- Accuracy of future resource usage predictions with different algorithms.

## What tools will we use?

- Kubernetes
- InfluxDB/Grafana
- Simulate web requests (Seagull)?

## Questions
- Is it ok for us to only test pods that are responding to HTTP requests? That
  is the majority of what Kubernetes is used for (focus on long running services)
  and also fits nicely with the focus on microservices.
- How do we normalize the summation of ERU and QOS so that both have an equal
  impact?
- Where will we get traffic request patterns from?
    - Seagull seems to be able to generate standardized traffic patterns.
      Although there may be a more current option than Seagull.
- How does Kubernetes reclaim unused CPU from pods? Should we be enforcing
  certain CPU reservation requirements? How will that inform how we measure CPU?
  (Include section on in evaluation).

