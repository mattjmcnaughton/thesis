# Trail Versioning

We ran multiple versions of our trials within different parameters for
predictive auto-scaling and Kubernetes.

- v1/unlabelled - This is the trial reflecting a standard Kubernetes deploy,
  with out addition of predictive auto-scaling. If a data point does not have a
  version attached, we assume it is part of v1.
- v2 - This is the trial in which we change the upscaleForbiddenWindow to `30
  seconds` instead of `3 minutes`.
- v3 - This is the trial in which we downscale predictively based on the 30
  second grace period, in addition to the `v2` changes.

## Specifying trial version when running trials

We will create configuration files for `test-server` which include the `VERSION`
env variable. So to run v2 trials with a 135s pod initialization time, run
`export TS_RC=test-server-controller-reactive-5s-v2.yaml; export ...; make run`.
Make sure that the appropriate version of the Kubernetes cluster is running.

## Specifying trial version when performing post-processing

We'll pass the version to `evaluate.py` as a command line argument. We'll use an
environment variable in our make task to specify the version, so run `export
PIT=5s; export TP=increase-decrease; export VERSION=v2; export OUT=/code/output; make process`
