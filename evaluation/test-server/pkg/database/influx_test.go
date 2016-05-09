package database_test

import (
	"github.com/mattjmcnaughton/test-server/pkg/database"
	"os"
	"testing"
)

// TestWriteMetrics confirms we are writing metrics to the database correctly.
func TestWriteMetrics(t *testing.T) {
	origQuery, err := database.QueryDatabase()

	if err != nil {
		t.Fatal(err.Error())
	}

	origCount := len(origQuery)

	writeToDatabase(t)

	afterQuery, err := database.QueryDatabase()

	if err != nil {
		t.Fatal(err.Error())
	}

	afterCount := len(afterQuery)

	if afterCount != origCount+1 {
		t.Fatalf("Should add one new elem, instead of adding %v, %v exist",
			afterCount-origCount, afterCount)
	}
}

// TestProperTags confirms we are recording the tags correctly.
func TestProperTags(t *testing.T) {
	writeToDatabase(t)

	afterQuery, err := database.QueryDatabase()
	if err != nil {
		t.Fatal(err.Error())
	}

	lastEntry := afterQuery[len(afterQuery)-1]

	found := false
	for _, tag := range lastEntry {
		if tag == os.Getenv("VERSION") {
			found = true
		}
	}

	if !found {
		t.Fatal("Should have found the VERSION tag.")
	}
}

func writeToDatabase(t *testing.T) {
	eru, qos, trafficPattern := 1.0, 1.0, "increase-decrease"
	err := database.WriteMetrics(eru, qos, trafficPattern)

	if err != nil {
		t.Fatal("Error writing metrics to the database.")
	}
}
