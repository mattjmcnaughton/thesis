package main

import (
	"github.com/codegangsta/negroni"
	"github.com/mattjmcnaughton/test-server/pkg/routers"
	"os"
)

const (
	// DefaultPort is the port on which to run the application if none is
	// specified in ENV.
	DefaultPort = "3000"

	// PortEnvVariable is the variable name of the PORT in env.
	PortEnvVariable = "PORT"
)

func main() {
	n := negroni.Classic()
	n.UseHandler(routers.GetNewMux())
	n.Run(":" + getPort())
}

// getPort returns the port on which the server should serve. For using Gin, and
// also for configuring different ports on k8s, it is important to first try and
// read the port from an environment variable.
func getPort() string {
	port := os.Getenv(PortEnvVariable)

	if port == "" {
		port = DefaultPort
	}

	return port
}
