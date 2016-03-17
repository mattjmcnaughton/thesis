package handlers_test

import (
	"github.com/mattjmcnaughton/test-server/pkg/routers"
	"net/http/httptest"
)

var (
	testServer *httptest.Server
)

func init() {
	router := routers.GetNewMux()
	testServer = httptest.NewServer(router)
}
