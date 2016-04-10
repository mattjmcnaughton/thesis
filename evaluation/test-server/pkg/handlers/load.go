package handlers

import (
	"encoding/json"
	"fmt"
	"github.com/mattjmcnaughton/test-server/pkg/database"
	"golang.org/x/crypto/bcrypt"
	"net/http"
	"os"
	"time"

	"github.com/stvp/roll"

	linuxproc "github.com/c9s/goprocinfo/linux"
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
		err = database.WriteMetrics(eru, qos)

		if err != nil {
			handleError(err, w, r)
		} else {
			// Output the response as JSON.
			w.WriteHeader(200)

			enc, err := json.Marshal(map[string]float64{
				"eru": eru,
				"qos": qos,
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
	initIdlePercent, err := idleCPUPercent()
	if err != nil {
		return 0.0, 0.0, err
	}

	initTime := time.Now()

	measureFunc()

	endIdlePercent, err := idleCPUPercent()
	if err != nil {
		return 0.0, 0.0, err
	}

	diffTime := time.Since(initTime)

	avgIdleCPUPercent := (initIdlePercent + endIdlePercent) / 2.0
	funcExecTime := diffTime.Seconds()

	return avgIdleCPUPercent, funcExecTime, nil
}

// costIntensiveTask is a useless task that is just required to take up CPU. We
// run it while so that the number of requests will have some kind of influence
// on the amount of pods needed.
func costIntensiveTask() {
	numPasswordsToGenerate := 2
	password := []byte("StartPassword")
	var err error

	for i := 0; i < numPasswordsToGenerate; i++ {
		password, err = bcrypt.GenerateFromPassword([]byte(password),
			bcrypt.DefaultCost)

		if err != nil {
			password = []byte("DefaultPassword")
		}
	}
}

// idleCPUPercent is a helper function to return the current percentage of CPU
// that is idle.
func idleCPUPercent() (float64, error) {
	// The use of `/proc/stat` assumes we are running on Linux, which is a
	// safe assumption to make.
	statFile := "/proc/stat"
	stat, err := linuxproc.ReadStat(statFile)
	if err != nil {
		return -1, err
	}

	allStat := stat.CPUStatAll

	// @TODO Are these the only ones I need to calculate total CPU?
	// There are the options -
	// https://godoc.org/github.com/c9s/goprocinfo/linux#CPUStat
	totalCPU := allStat.User + allStat.Nice + allStat.System + allStat.Idle +
		allStat.IOWait + allStat.IRQ + allStat.Guest

	percentIdle := float64(allStat.Idle) / float64(totalCPU)

	return percentIdle, nil
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
