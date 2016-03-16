package handlers

import (
	//#include <time.h>
	"C"

	"encoding/json"
	"github.com/mattjmcnaughton/test-server/pkg/database"
	"golang.org/x/crypto/bcrypt"
	"net/http"
	"time"
)

// LoadHandler is the handler for the request to "/". It is to this api endpoint
// that we will send the traffic patterns to test auto-scaling. This endpoint
// first performs some relatively substantial amount of computational work that
// will utilize a portion of the CPU, and then writes the CPU utilization for
// the pod and some metric measuring of quality of service, such as how long it
// took the pod to perform the previous computation.
func LoadHandler(w http.ResponseWriter, r *http.Request) {
	eru, qos := measureExecTimeAndCPU(costIntensiveTask)
	err := database.WriteMetrics(eru, qos)

	if err != nil {
		w.WriteHeader(500)
		w.Write([]byte(err.Error()))
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

	return
}

// measureExecTimeAndCPU is a helper method that takes a function and runs it,
// while measuring the amount of time it takes to execute and the percent of CPU
// the processes uses while executing.
// @TODO It would be great if there was a way to measure CPU usage that didn't
// require running C code from golang.
func measureExecTimeAndCPU(measureFunc func()) (float64, float64) {
	initTime := time.Now()
	initTicks := C.clock()

	measureFunc()

	diffTime := time.Since(initTime)
	diffTicks := float64(C.clock()-initTicks) / float64(C.CLOCKS_PER_SEC)

	funcExecTime := diffTime.Seconds()

	// @TODO Does CPU percentage have to be divided by cores?
	cpuUsagePercentage := (diffTicks / funcExecTime) * 100.0

	return funcExecTime, cpuUsagePercentage
}

// costIntensiveTask is a useless task that is just required to take up CPU. We
// run it while so that the number of requests will have some kind of influence
// on the amount of pods needed.
func costIntensiveTask() {
	numPasswordsToGenerate := 10
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
