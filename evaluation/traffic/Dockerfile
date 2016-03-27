# Dockerfile for packaging traffic generation into a container that can be run
# in a k8s pod.

FROM rdpanek/jmeter

ADD test-plans /test-plans
ADD scripts /scripts

WORKDIR /test-plans

# Ensure the script is executable
RUN chmod a+x /scripts/start-jmeter.sh

# Run the test plan specified by the `TEST_PLAN` env variable which will be set
# in the Kubernetes yaml file for the pod.
CMD ["sh", "/scripts/start-jmeter.sh"]
