package handlers_test

import (
	"fmt"
	"net/http"
	"testing"
)

func TestLoad(t *testing.T) {
	req, err := http.NewRequest("GET", fmt.Sprintf("%s/", testServer.URL), nil)
	res, err := http.DefaultClient.Do(req)

	if err != nil {
		t.Fatal("Get request to / resulted in error.")
	}

	if res.StatusCode != http.StatusOK {
		t.Fatalf("Get request to / should return 200, not %v",
			res.StatusCode)
	}
}
