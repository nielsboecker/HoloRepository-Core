package holostorageaccessor

import (
	"encoding/json"
	"fmt"
	"log"
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
					"id": "p2000",
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
								"Ms"
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
				statusCode = http.StatusInternalServerError
				fmt.Println("I received this:", rcvURL)
			}
		}

		w.WriteHeader(statusCode)
		fmt.Fprintf(w, response)
	}))

	return ts
}

func TestMultipleAuthorsGet(t *testing.T) {
	type test struct {
		wantStatus int
		wantBody   map[string]Author
		wantErr    Error
		inUrl      string
		inMethod   string
	}

	tests := map[string]test{
		"no_aids_query": {
			inUrl:      "/api/v1/authors",
			inMethod:   http.MethodGet,
			wantStatus: 400,
		},
		"wrong_query_field": {
			inUrl:      "/api/v1/authors?aid=a1000",
			inMethod:   http.MethodGet,
			wantStatus: 400,
		},
		"single_found_author": {
			inUrl:      "/api/v1/authors?aids=a1000",
			inMethod:   http.MethodGet,
			wantStatus: 200,
			wantBody: map[string]Author{
				"a1000": Author{
					Aid: "a1000",
					Name: &PersonName{
						Family: "Campbell",
						Full:   "Roy Campbell",
						Given:  "Roy",
						Title:  "Mr",
					},
				},
			},
		},
		"single_missing_author": {
			inUrl:      "/api/v1/authors?aids=a3000",
			inMethod:   http.MethodGet,
			wantStatus: 200,
			wantBody: map[string]Author{
				"a3000": Author{},
			},
		},
		"found_author": {
			inUrl:      "/api/v1/authors?aids=a1000,a2000,a3000",
			inMethod:   http.MethodGet,
			wantStatus: 200,
			wantBody: map[string]Author{
				"a1000": Author{
					Aid: "a1000",
					Name: &PersonName{
						Family: "Campbell",
						Full:   "Roy Campbell",
						Given:  "Roy",
						Title:  "Mr",
					},
				},
				"a2000": Author{
					Aid: "a2000",
					Name: &PersonName{
						Family: "Sawyer",
						Full:   "Tom Sawyer",
						Given:  "Tom",
						Title:  "Mr",
					},
				},
				"a3000": Author{},
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

			if tc.wantBody != nil {
				var authorData map[string]Author
				err := json.Unmarshal(w.Body.Bytes(), &authorData)
				if err != nil {
					t.Fatalf("Unmarshal Author error: %s", err.Error())
				}
				diff = cmp.Diff(tc.wantBody, authorData)
			} else if (tc.wantErr != Error{}) {
				var errorData Error
				err := json.Unmarshal(w.Body.Bytes(), &errorData)
				if err != nil {
					t.Logf(string(w.Body.Bytes()))
					t.Fatalf("Unmarshal Error error: %s", err.Error())
				}
				diff = cmp.Diff(tc.wantErr, errorData)
			}

			if diff != "" {
				t.Fatalf(diff)
			}
		})
	}

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
					t.Fatalf("Unmarshal Author error: %s", err.Error())
				}
				diff = cmp.Diff(tc.wantBody, authorData)
			} else if (tc.wantErr != Error{}) {
				var errorData Error
				err := json.Unmarshal(w.Body.Bytes(), &errorData)
				if err != nil {
					t.Fatalf("Unmarshal Error error: %s", err.Error())
				}
				diff = cmp.Diff(tc.wantErr, errorData)
			}

			if diff != "" {
				t.Fatalf(diff)
			}
		})
	}
}

func TestMultiplePatientsGet(t *testing.T) {
	type test struct {
		wantStatus int
		wantBody   map[string]Patient
		wantErr    Error
		inUrl      string
		inMethod   string
	}

	tests := map[string]test{
		"no_aids_query": {
			inUrl:      "/api/v1/patients",
			inMethod:   http.MethodGet,
			wantStatus: 400,
		},
		"wrong_query_field": {
			inUrl:      "/api/v1/patients?pid=p1000",
			inMethod:   http.MethodGet,
			wantStatus: 400,
		},
		"single_found_patient": {
			inUrl:      "/api/v1/patients?pids=p1000",
			inMethod:   http.MethodGet,
			wantStatus: 200,
			wantBody: map[string]Patient{
				"p1000": Patient{
					Pid:       "p1000",
					Gender:    "male",
					BirthDate: "1990-10-10",
					Name: &PersonName{
						Family: "Jones",
						Full:   "Timothy Jones",
						Given:  "Timothy",
						Title:  "Mr",
					},
				},
			},
		},
		"single_missing_patient": {
			inUrl:      "/api/v1/patients?pids=p3000",
			inMethod:   http.MethodGet,
			wantStatus: 200,
			wantBody: map[string]Patient{
				"p3000": Patient{},
			},
		},
		"found_patient": {
			inUrl:      "/api/v1/patients?pids=p1000,p2000,p3000",
			inMethod:   http.MethodGet,
			wantStatus: 200,
			wantBody: map[string]Patient{
				"p1000": Patient{
					Pid:       "p1000",
					Gender:    "male",
					BirthDate: "1990-10-10",
					Name: &PersonName{
						Family: "Jones",
						Full:   "Timothy Jones",
						Given:  "Timothy",
						Title:  "Mr",
					},
				},
				"p2000": Patient{
					Pid:       "p2000",
					Gender:    "female",
					BirthDate: "1960-01-02",
					Name: &PersonName{
						Family: "Spears",
						Given:  "Britney",
						Title:  "Ms",
					},
				},
				"p3000": Patient{},
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

			if tc.wantBody != nil {
				var patientData map[string]Patient
				err := json.Unmarshal(w.Body.Bytes(), &patientData)
				if err != nil {
					t.Fatalf("Unmarshal Patient error: %s", err.Error())
				}
				diff = cmp.Diff(tc.wantBody, patientData)
			} else if (tc.wantErr != Error{}) {
				var errorData Error
				err := json.Unmarshal(w.Body.Bytes(), &errorData)
				if err != nil {
					t.Logf(string(w.Body.Bytes()))
					t.Fatalf("Unmarshal Error error: %s", err.Error())
				}
				diff = cmp.Diff(tc.wantErr, errorData)
			}

			if diff != "" {
				t.Fatalf(diff)
			}
		})
	}

}

func TestPatientsPidGet(t *testing.T) {
	type test struct {
		wantStatus int
		wantBody   Patient
		wantErr    Error
		inUrl      string
		inMethod   string
	}

	tests := map[string]test{
		"found_patient": {
			inUrl:      "/api/v1/patients/p1000",
			inMethod:   http.MethodGet,
			wantStatus: 200,
			wantBody: Patient{
				Pid:       "p1000",
				Gender:    "male",
				BirthDate: "1990-10-10",
				Name: &PersonName{
					Family: "Jones",
					Full:   "Timothy Jones",
					Given:  "Timothy",
					Title:  "Mr",
				},
			},
		},
		"missing_patient": {
			inUrl:      "/api/v1/patients/p3000",
			inMethod:   http.MethodGet,
			wantStatus: 404,
			wantErr: Error{
				ErrorCode:    "404",
				ErrorMessage: `id 'p3000' cannot be found`,
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

			if (tc.wantBody != Patient{}) {
				var patientData Patient
				err := json.Unmarshal(w.Body.Bytes(), &patientData)
				if err != nil {
					t.Fatalf("Unmarshal Patient error: %s", err.Error())
				}
				diff = cmp.Diff(tc.wantBody, patientData)
			} else if (tc.wantErr != Error{}) {
				var errorData Error
				err := json.Unmarshal(w.Body.Bytes(), &errorData)
				if err != nil {
					t.Logf(string(w.Body.Bytes()))
					t.Fatalf("Unmarshal Error error: %s", err.Error())
				}
				diff = cmp.Diff(tc.wantErr, errorData)
			}

			if diff != "" {
				t.Fatalf(diff)
			}
		})
	}
}
