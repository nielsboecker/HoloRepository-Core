package holostorageaccessor

import (
	"encoding/json"
	"fmt"
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/google/go-cmp/cmp"
)

func setupTestServer() *httptest.Server {
	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		var response string
		var statusCode = http.StatusOK

		if r.Method == "GET" {
			switch rcvURL := r.URL.String(); rcvURL {
			case "/Patient/p1000":
				statusCode = http.StatusOK
				response = `{
					"resourceType": "Patient",
					"id": "p1000",
					"meta": {
						"versionId": "9",
						"lastUpdated": "2019-08-08T22:20:52.729+00:00"
					},
					"name": [
						{
							"text": "Timothy Jones",
							"family": "Jones",
							"given": [
								"Timothy"
							],
							"prefix": [
								"Mr"
							]
						}
					],
					"gender": "male",
					"birthDate": "1990-10-10"
				}`
			case "/Patient/p2000":
				statusCode = http.StatusOK
				response = `{
					"resourceType": "Patient",
					"id": "p102",
					"meta": {
						"versionId": "1",
						"lastUpdated": "2019-08-08T21:57:58.323+00:00"
					},
					"name": [
						{
							"use": "official",
							"family": "Spears",
							"given": [
								"Britney"
							],
							"prefix": [
								"Mr"
							]
						}
					],
					"gender": "female",
					"birthDate": "1960-01-02"
				}`
			case "/Patient/p3000":
				statusCode = http.StatusNotFound
				response = `{
					"resourceType": "OperationOutcome",
					"id": "5aa08306-f01f-47ea-8250-70cb9932c6ac",
					"issue": [
						{
							"severity": "error",
							"code": "not-found",
							"diagnostics": "Resource type 'Patient' with id 'p3000' couldn't be found."
						}
					]
				}`
			case "/Practitioner/a1000":
				statusCode = http.StatusOK
				response = `{
					"resourceType": "Practitioner",
					"id": "a1000",
					"meta": {
						"versionId": "7",
						"lastUpdated": "2019-08-08T23:02:44.88+00:00"
					},
					"name": [
						{
							"text": "Roy Campbell",
							"family": "Campbell",
							"given": [
								"Roy"
							],
							"prefix": [
								"Mr"
							]
						}
					]
				}`
			case "/Practitioner/a2000":
				statusCode = http.StatusOK
				response = `{
					"resourceType": "Practitioner",
					"id": "a2000",
					"meta": {
						"versionId": "26",
						"lastUpdated": "2019-08-11T02:04:38.235+00:00"
					},
					"name": [
						{
							"text": "Tom Sawyer",
							"family": "Sawyer",
							"given": [
								"Tom"
							],
							"prefix": [
								"Mr"
							]
						}
					]
				}`
			case "/Practitioner/a3000":
				statusCode = http.StatusNotFound
				response = `{
					"resourceType": "OperationOutcome",
					"id": "73f97942-f6da-4f02-ac81-2b9bc8be9fcf",
					"issue": [
						{
							"severity": "error",
							"code": "not-found",
							"diagnostics": "Resource type 'Practitioner' with id 'a20000' couldn't be found."
						}
					]
				}`
			default:
				fmt.Println("I received this:", rcvURL)
			}
		}

		w.WriteHeader(statusCode)
		fmt.Fprintf(w, response)
	}))

	return ts
}

func TestAuthorsAidGet(t *testing.T) {
	type test struct {
		wantStatus int
		wantBody   Author
		wantErr    Error
		inUrl      string
		inMethod   string
	}

	tests := map[string]test{
		"found_author": {
			inUrl:      "/api/v1/authors/a1000",
			inMethod:   http.MethodGet,
			wantStatus: 200,
			wantBody: Author{
				Aid: "a1000",
				Name: &PersonName{
					Family: "Campbell",
					Full:   "Roy Campbell",
					Given:  "Roy",
					Title:  "Mr",
				},
			},
		},
		"missing_author": {
			inUrl:      "/api/v1/authors/a3000",
			inMethod:   http.MethodGet,
			wantStatus: 404,
			wantErr: Error{
				ErrorCode:    "404",
				ErrorMessage: `id 'a3000' cannot be found`,
			},
		},
	}

	// Start a local HTTP server and Router
	ts := setupTestServer()
	defer ts.Close()
	router := NewRouter(AccessorConfig{FhirURL: ts.URL})

	for name, tc := range tests {
		t.Run(name, func(t *testing.T) {
			diff := ""
			req, _ := http.NewRequest(tc.inMethod, tc.inUrl, nil)
			w := httptest.NewRecorder()
			router.ServeHTTP(w, req)

			if tc.wantStatus != w.Code {
				t.Fatalf("Error return code: Want %d, got %d", tc.wantStatus, w.Code)
			}

			if (tc.wantBody != Author{}) {
				var authorData Author
				err := json.Unmarshal(w.Body.Bytes(), &authorData)
				if err != nil {
					t.Fatalf(err.Error())
				}
				diff = cmp.Diff(tc.wantBody, authorData)
			} else if (tc.wantErr != Error{}) {
				var errorData Error
				err := json.Unmarshal(w.Body.Bytes(), &errorData)
				if err != nil {
					t.Fatalf(err.Error())
				}
				diff = cmp.Diff(tc.wantErr, errorData)
			}

			if diff != "" {
				t.Fatalf(diff)
			}
		})
	}

}
