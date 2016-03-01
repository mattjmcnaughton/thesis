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
- gnu-plot (Graphing)
- Simulate web requests (Apache jmeter)?

## Questions
- Is it ok for us to only test pods that are responding to HTTP requests? That
  is the majority of what Kubernetes is used for (focus on long running services)
  and also fits nicely with the focus on microservices.
- How do we normalize the summation of ERU and QOS so that both have an equal
  impact?
- Where will we get traffic request patterns from?
- How does Kubernetes reclaim unused CPU from pods? Should we be enforcing
  certain CPU reservation requirements? How will that inform how we measure CPU?
  (Include section on in evaluation).

