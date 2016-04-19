package handlers

import (
	"bytes"
	"encoding/json"
	"errors"
	"fmt"
	"github.com/mattjmcnaughton/test-server/pkg/database"
	"golang.org/x/crypto/bcrypt"
	"net/http"
	"os"
	"os/exec"
	"strconv"
	"strings"
	"time"

	"github.com/stvp/roll"
)

const (
	// RollbarTokenVariable is the name of the evironment variable that we
	// use to store to Rollbar server-side access token.
	RollbarTokenVariable = "ROLLBAR_TOKEN"

	// EnvVariable is the name of the environment variable we use to
	// indicate which environment we are running in.
	EnvVariable = "TEST_SERVER_ENV"

	// EnvProduction is the value for the os environment variable
	// `TEST_SERVER_ENV` if running production mode.
	EnvProduction = "PRODUCTION"

	// TrafficPatternParam is the parameter
	// `?traffic-pattern=increase-decrease` identifying the Traffic Pattern
	// being used for this evaluation.
	TrafficPatternParam = "traffic-pattern"
)

// LoadHandler is the handler for the request to "/". It is to this api endpoint
// that we will send the traffic patterns to test auto-scaling. This endpoint
// first performs some relatively substantial amount of computational work that
// will utilize a portion of the CPU, and then writes the CPU utilization for
// the pod and some metric measuring of quality of service, such as how long it
// took the pod to perform the previous computation.
func LoadHandler(w http.ResponseWriter, r *http.Request) {
	eru, qos, err := profileFunction(costIntensiveTask)

	if err != nil {
		handleError(err, w, r)
	} else {
		trafficPattern := r.URL.Query().Get(TrafficPatternParam)
		err = database.WriteMetrics(eru, qos, trafficPattern)

		if err != nil {
			handleError(err, w, r)
		} else {
			// Output the response as JSON.
			w.WriteHeader(200)

			enc, err := json.Marshal(map[string]interface{}{
				"eru":             eru,
				"qos":             qos,
				"traffic-pattern": trafficPattern,
			})

			if err == nil {
				w.Write(enc)
			}
		}
	}

	return
}

// profileFunction is a helper method that takes a function and runs it,
// while measuring the percent of CPU the processes uses while executing and the
// amount of time it takes to execute.
//
// We measure ERU by recording the percent of idle CPU time. So if efficient
// resource utilization is doing well, then we want this value to be low.
func profileFunction(measureFunc func()) (eru float64, qos float64, err error) {
	if err != nil {
		return 0.0, 0.0, err
	}

	initTime := time.Now()

	measureFunc()

	diffTime := time.Since(initTime)

	cpuPercent, err := idleCPUPercent()
	if err != nil {
		return 0.0, 0.0, err
	}

	funcExecTime := diffTime.Seconds()
	return cpuPercent, funcExecTime, nil
}

// costIntensiveTask is a useless task that is just required to take up CPU. We
// run it while so that the number of requests will have some kind of influence
// on the amount of pods needed.
func costIntensiveTask() {
	numPasswordsToGenerate := 3
	password := []byte("StartPassword")
	var err error

	for i := 0; i < numPasswordsToGenerate; i++ {
		password, err = bcrypt.GenerateFromPassword([]byte(password),
			bcrypt.MinCost)

		if err != nil {
			password = []byte("DefaultPassword")
		}
	}
}

// idleCPUPercent is a helper function to return the current percentage of CPU
// that is idle.
// We check it using `top`. We use -n 2 to do 2 iterations, and make sure that
// we don't just use the first observation, because it returns the average up to
// this point.
func idleCPUPercent() (float64, error) {
	cpuCmd := "top -b -n 2 -d .5 | grep \"Cpu\" | tail -n1 | awk -F ',' '{print($4)}' | cut -d 'i' -f 1"
	var stderr bytes.Buffer

	cmd := exec.Command("bash", "-c", cpuCmd)
	cmd.Stderr = &stderr

	cmdOut, err := cmd.Output()
	if err != nil {
		err = errors.New(err.Error() + ": " + stderr.String())
		return 0.0, err
	}

	// cmdOut contains just the value for idle cpu so we can get the string
	// and then try to parse it as a float - be sure to remove the new line.
	cpuStr := strings.Trim(string(cmdOut), " \n")

	cpu, err := strconv.ParseFloat(cpuStr, 64)
	if err != nil {
		return 0.0, err
	}

	return cpu, nil
}

// handleError is a helper function which, given an error during a http request,
// writes 500 and the contents of the error, in addition to printing to log the
// error, and recording it in rollbar.
func handleError(err error, w http.ResponseWriter, r *http.Request) {
	if inProduction() {
		recordRollbar(err)
	}

	fmt.Printf("The following error occurred: %v", err.Error())

	w.WriteHeader(500)
	w.Write([]byte(err.Error()))
}

// inProduction checks if we are currently operating in production mode.
// Production mode is set with `TEST_SERVER_ENV=PRODUCTION`
func inProduction() bool {
	return os.Getenv(EnvVariable) == EnvProduction
}

// recordRollbar records an error to the Rollbar aggregation service.
func recordRollbar(err error) {
	client := roll.New(os.Getenv(RollbarTokenVariable), EnvProduction)

	_, rollbarErr := client.Error(err, map[string]string{})
	if rollbarErr != nil {
		fmt.Printf("Got the error %v recording the error %v to Rollbar.\n",
			rollbarErr, err)
	}
}
