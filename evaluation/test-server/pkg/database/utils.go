package database

import (
	"fmt"
	client "github.com/influxdata/influxdb/client/v2"
	"log"
	"os"
)

const (
	// PointName is the name for this type of point in influxdb.
	PointName = "METRICS"
)

var (
	// Configure all of this environment specific environmation through
	// `.env` files, or `ENV` info in Kubernetes yaml files.
	databaseName     = os.Getenv("DATABASE_NAME")
	databaseAddress  = os.Getenv("DATABASE_ADDRESS")
	databaseUsername = os.Getenv("DATABASE_USERNAME")
	databasePassword = os.Getenv("DATABASE_PASSWORD")

	// The method of auto-scaling and pit in use for this container.
	scalingMethod         = os.Getenv("SCALING_METHOD")
	podInitializationTime = os.Getenv("INITIALIZATION_TIME")
)

// createClient is an internal method for creating a HTTP Connection to the database.
func createClient() (client.Client, error) {
	config := client.HTTPConfig{
		Addr:     databaseAddress,
		Username: databaseUsername,
		Password: databasePassword,
	}

	influxClient, err := client.NewHTTPClient(config)

	if err != nil {
		log.Println("Error creating an HTTP Client for Influx.")
		return nil, err
	}

	return influxClient, nil
}

// QueryDatabase is a helper method usable by other packages to query the
// database to check that something has been written. It returns the actual
// results that are written, not the query object.
func QueryDatabase() ([][]interface{}, error) {
	influxClient, err := createClient()

	if err != nil {
		log.Println(err.Error())
		return nil, err
	}

	defer influxClient.Close()

	query := client.Query{
		Database: databaseName,
		Command:  fmt.Sprintf("SELECT * FROM %s", PointName),
	}
	response, err := influxClient.Query(query)

	if err != nil {
		return nil, err
	}

	if response.Error() != nil {
		return nil, response.Error()
	}
	return response.Results[0].Series[0].Values, nil
}
