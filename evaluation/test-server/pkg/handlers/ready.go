package handlers

import (
	"net/http"
	"os"
	"time"
)

const (
	// InitTimeEnvVariable is variable name in the ENV.
	InitTimeEnvVariable = "INITIALIZATION_TIME"
)

// ReadyHandler is the handler for the request to "/ready". The container uses
// this endpoint as the ReadinessProbe, as a response of success indicates that
// the pod is ready.
//
// @TODO Is there a better method of implementing this than just waiting a
// really long time to return? Maybe instead we could record when the first
// request came in (in the database) and not return success. We would return
// success only when receiving a request after `INIT_TIME` had passed.
func ReadyHandler(w http.ResponseWriter, r *http.Request) {
	// Anonymous function to return a successful response after the proper
	// interval of time passes.
	successFunc := func() {
		w.WriteHeader(200)
		return
	}

	// @TODO Include a better method of error checking.
	dur, _ := time.ParseDuration(os.Getenv(InitTimeEnvVariable))
	_ = time.AfterFunc(dur, successFunc)
}
