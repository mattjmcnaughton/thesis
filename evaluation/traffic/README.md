# Traffic

This directory contains the documentation and configuration files necessary for
generating the patterned traffic with which we will test the different scaling
options.

We generate requests using Apache JMeter, and more specifically the `Throughput
Shaping Timer` plugin, which allows us to specify a request throughput pattern
and have JMeter send requests to fit this pattern.

We containerize JMeter and run it on Kubernetes so that we are not sending all
of these requests from a local machine. We are careful to set strict resource
limits so that JMeter does not hog CPU.
