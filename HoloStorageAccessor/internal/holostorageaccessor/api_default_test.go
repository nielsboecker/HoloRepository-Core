package holostorageaccessor

import (
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"net/http/httptest"
	"testing"
)

func setupTestServer() *httptest.Server {
	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		fmt.Println(r.URL.String())
		fmt.Fprintln(w, "Hello, client")
	}))

	return ts
}

func TestAuthorsAidGet(t *testing.T) {
	// Start a local HTTP server
	ts := setupTestServer()

	defer ts.Close()

	res, err := http.Get(ts.URL)
	if err != nil {
		t.Fatal(err)
	}

	greeting, err := ioutil.ReadAll(res.Body)
	res.Body.Close()
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("%s", greeting)

	// Use Client & URL from our local test server
	router := NewRouter(AccessorConfig{FhirURL: ts.URL})

	w := httptest.NewRecorder()
	req, _ := http.NewRequest("GET", "/api/v1/authors/a123", nil)

	router.ServeHTTP(w, req)

	fmt.Println("recorder:", w)
}
