package database

import (
	client "github.com/influxdata/influxdb/client/v2"
	"log"
	"os"
	"time"
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

	// The method of auto-scaling in use for this container.
	scalingMethod = os.Getenv("SCALING_METHOD")
)

// Internal method for creating a HTTP Connection to the database.
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

// WriteMetrics is called from a handler to write the eru and qos metrics to the
// influxdb database.
func WriteMetrics(eru, qos float64) error {
	influxClient, err := createClient()

	if err != nil {
		log.Println("Error getting the HTTP client for Influx.")
		return err
	}

	// After this function terminates, close the HTTP client connection.
	defer influxClient.Close()

	bp, _ := client.NewBatchPoints(client.BatchPointsConfig{
		Database: databaseName,
		// @TODO Does "s" make sense
		Precision: "s",
	})

	tags := map[string]string{"scaling-method": scalingMethod}
	fields := map[string]interface{}{
		"eru": eru,
		"qos": qos,
	}

	pt, err := client.NewPoint(PointName, tags, fields, time.Now())
	if err != nil {
		log.Println("Error creating the new point.")
		return err
	}

	bp.AddPoint(pt)

	return influxClient.Write(bp)
}
