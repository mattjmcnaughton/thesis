package database

import (
	client "github.com/influxdata/influxdb/client/v2"
	"log"
	"time"
)

// WriteMetrics is called from a handler to write the eru and qos metrics to the
// influxdb database.
func WriteMetrics(eru, qos float64, trafficPattern string) error {
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

	tags := map[string]string{
		"sm":  scalingMethod,
		"tp":  trafficPattern,
		"pit": podInitializationTime,
		"ver": version,
	}
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
