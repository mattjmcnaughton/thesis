package database_test

import (
	"github.com/mattjmcnaughton/test-server/pkg/database"
	"testing"
)

func TestWriteMetrics(t *testing.T) {
	origQuery, err := database.QueryDatabase()

	if err != nil {
		t.Fatal(err.Error())
	}

	origCount := len(origQuery)

	eru, qos := 1.0, 1.0
	err = database.WriteMetrics(eru, qos)

	if err != nil {
		t.Fatal("Error writing metrics to the database.")
	}

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
