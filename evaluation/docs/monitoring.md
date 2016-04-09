# Monitoring

It is important to ensure that my evaluation tests are running error free. This
document includes commands for monitoring each components of the evaluation
process to ensure it is occurring as expected.

## Kubernetes

The main errors I want to watch out for are:
- `FailedScheduling: Node didn't have enough resource: CPU, ...`, which
  indicates that I do not have enough resources to auto-scale.
- `HorizontalPodAutoscaler`: Any error from my predictive auto-scaling
  implementation will have `HorizontalPodAutoscaler` (or something similar) as
  the annotation. Since this code is not as tested as the other code, I want to
  be especially cognizant of these errors.

Kubernetes does not have a particularly great mechanism for only be alerted when
these errors arise. I think my best option is to watch the logs during
tests/review them after using `kubectl get --watch events` and `kubectl get
events`. I can use `grep` to search for `FailedScheduling` and
`HorizontalPodAutoscaler` keywoards.

## test-server

There are a couple of options for checking if `test-server` is working
correctly. To start, we've set up `Rollbar` to record errors and to send email
notifications if a substantial number of errors occur. Errors can also be viewed
from the `Rollbar` dashboard. In addition, it is
possible to tail logs on individual pods using `kubectl logs -f POD_NAME`.
Finally, we can use [kubetail](https://github.com/johanhaleby/kubetail) to tail
the logs for all pods associated with the `test-server` replication controller.

The main errors to watch out for are:
- Errors writing to the database.
- If request times are exceptionally long.

## traffic-generator

For the `traffic-generator` we want to keep track of how many of sent requests
are responded to/successful and also make sure that we aren't trying to send to
many requests per second with respect to how many threads we have (although I'm
not really worried about this because I think our cap on requests per second
will be `test-server`, not the number of threads available). We can again use
`kubectl logs -f TRAFFIC_POD_NAME` to watch jmeter's logs and also track what
percent of requests are successful. If we are worried about running out of
threads, then we will need to use something different than `kubectl logs -f ...`
but I'm really not worried about that happening because I think we're sending a
very low volume of request. We should also be able to tell approximately how
many requests are being sent passed on what `jmeter` looks to `stdout`.
