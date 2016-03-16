package handlers

import (
	// #include <time.h>
	"C"

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
	database.WriteMetrics(eru, qos)

	w.WriteHeader(200)
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
	diffTicks := float64(C.clock()-initTicks) / float64(C.CLOCKS_PER_SECOND)

	funcExecTime := diffTime.Seconds()
	cpuUsagePercentage := (diffTicks / diffTime) * 100.0

	return funcExecTime, cpuUsagePercentage
}

// costIntensiveTask is a useless task that is just required to take up CPU. We
// run it while so that the number of requests will have some kind of influence
// on the amount of pods needed.
func costIntensiveTask() {
	numPasswordsToGenerate := 100
	password := []byte("StartPassword")
	var err error

	for i := 0; i < numPasswordsToGenerate; i++ {
		password, err = bcrypt.GenerateFromPassword([]byte(password),
			bcrypt.MaxCost)

		if err != nil {
			password = []byte("DefaultPassword")
		}
	}
}
