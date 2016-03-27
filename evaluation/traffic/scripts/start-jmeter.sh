# A simple script to start JMeter. We use the script only because it is
# otherwise a little buggy to try and get Docker to use an `ENV` variable in
# command, and the work around seems to cause `jmeter` to ignore its flags.

/srv/var/jmeter/apache-jmeter-2.12/bin/jmeter -n -t /test-plans/${TEST_PLAN}
