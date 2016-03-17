package handlers_test

import (
	"fmt"
	"github.com/mattjmcnaughton/test-server/pkg/handlers"
	"net/http"
	"os"
	"testing"
	"time"
)

func TestReady(t *testing.T) {
	startTime := time.Now()

	req, err := http.NewRequest("GET", fmt.Sprintf("%s/ready", testServer.URL), nil)
	res, err := http.DefaultClient.Do(req)

	if err != nil {
		t.Fatal("Get request to /ready resulted in error.")
	}

	if res.StatusCode != http.StatusOK {
		t.Fatalf("Get reqquest to /ready should return 200, not %v",
			res.StatusCode)
	}

	dur, _ := time.ParseDuration(os.Getenv(handlers.InitTimeEnvVariable))

	if dur > time.Since(startTime) {
		t.Fatalf("Did not wait the proper duration before returning.")
	}
}
