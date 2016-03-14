package handlers

import (
	"net/http"
	// Import database
)

// LoadHandler is the handler for the request to "/". It is to this api endpoint
// that we will send the traffic patterns to test auto-scaling. This endpoint
// first performs some relatively substantial amount of computational work that
// will utilize a portion of the CPU, and then writes the CPU utilization for
// the pod and some metric measuring of quality of service, such as how long it
// took the pod to perform the previous computation.
func LoadHandler(w http.ResponseWriter, r *http.Request) {
	// Perform CPU intensive computation.

	// Calcuate efficient resource utilization and quality of service

	// Write values to the database - the `database` pkg should define an
	// easy method for writing the values that abstracts all parts of the
	// database.
}
