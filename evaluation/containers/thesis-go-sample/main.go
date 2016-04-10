package main

import (
	"net/http"
	"os"
)

const (
	// DefaultPort is the port to use if not port is specified as an
	// environment variable.
	DefaultPort = "3000"

	// PortEnvVariable is the environment variable in which we look for a
	// port.
	PortEnvVariable = "PORT"
)

// index simply returns success showing that the server has initialized and is
// ready to serve requests.
func index(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(200)
	w.Write([]byte(""))

	return
}

// main runs an http server.
func main() {
	http.HandleFunc("/", index)
	http.ListenAndServe(":"+getPort(), nil)
}

// getPort returns the port on which the server should listen, allowing us to
// set the port through an environment variable.
func getPort() string {
	port := os.Getenv(PortEnvVariable)

	if port == "" {
		port = DefaultPort
	}

	return port
}
