# Creating Test Plan

This document describes a description of how to use `jmeter` create a test plan (a test plan
generates traffic to `test-server`).

- Open jmeter with `$ jmeter` (don't run this command from `tmux` - it won't
  work).
  - Open the file `../sample-test-plan.jsx`
- Rename the test plan from `sample-test-plan` to, for example,
  `flash-crowd-test-plan` and update the description.
  - Do not modify the `Ultimate Thread Group` field, unless needing to update
    the length of the test or increasing the request per second of the
    throughput such that we need more threads - this can be calculated using
    this [method](http://jmeter-plugins.org/wiki/ThroughputShapingTimer/).
  - Do not modify `HTTP Request Defaults`, unless changing the `Server Name or
    IP` field. Because we are using Kubernetes internal DNS, we will always
    refer to our service by the same name, and thus this value should not need
    to be updated.
  - We should need not to modify `HTTP Request`.
  - Modify `Throughput Shaping Timer` with whatever pattern we are testing.
    **Currently the length of all tests is 60 minutes, and the largest amount of
    requests per second we ever send is 500** so do not deviate from these
    values. @TODO Right now these constraints have little grounding, so come up
    with better ones or have a justification.
- Save the plan in the `../test-plan` directory under the following convention
  `PATTERN_NAME-test-plan.jsx`.
