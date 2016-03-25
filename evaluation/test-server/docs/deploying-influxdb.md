# Deploying InfluxDB

## Deploying InfluxDB instance

- Creating an instance to deploy is as simple as specifying the region on the
  `InfluxDB` dashboard.
- Login to the database as the admin user `influxdb` with the given password.
- Create a user entitled `mattjmcnaughton` with a specific password using the
  `admin dashboard`.
  - Grant this user all privileges with `GRANT ALL PRIVILEGES TO mattjmcnaughton`
- Create a database entitled `test-server-prod` with the admin dashboard.

## Configuring influxDB in an application
- Use the `mattjmcnaughton` username and password to specify as env variables
  the username and password for the HTTP client.
- Each database instance is given a host name, so be sure to specify the
  hostname as an env variable as well.

## Viewing Results

- Use the query `SELECT * from METRICS` when using the database
  `test-server-prod` to see the all of the database entries.
