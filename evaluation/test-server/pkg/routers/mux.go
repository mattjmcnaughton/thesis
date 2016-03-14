package routers

import (
	"net/http"

	"github.com/mattjmcnaughton/test-server/pkg/handlers"
)

// GetNewMux returns a new request routing Mux.
func GetNewMux() *http.ServeMux {
	mux := http.NewServeMux()

	mux.HandleFunc("/", handlers.LoadHandler)
	mux.HandleFunc("/ready", handlers.ReadyHandler)

	return mux
}
