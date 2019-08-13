package holostorageaccessor

import (
	"bytes"
	"encoding/json"
	"fmt"
	"log"
	"net"
	"net/http"
	"net/http/httptest"
	"net/url"
	"strings"
	"testing"

	"github.com/google/go-cmp/cmp"
)

func setupTestServer() *httptest.Server {
	baseurl := "127.0.0.1:2500"
	ts := httptest.NewUnstartedServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		var response string
		var statusCode = http.StatusOK

		wantHeaders := map[string]string{
			"Content-Type": "application/fhir+json",
		}
		switch r.Method {
		case "PUT", "POST":
			for header, want := range wantHeaders {
				gotHeader := r.Header.Get(header)
				if gotHeader != want {
					log.Fatalf("Invalid Content-Type: Want %q, got %q", want, gotHeader)
				}
			}
		}

		if r.Method == "GET" {
			switch rcvURL, _ := url.QueryUnescape(r.URL.String()); rcvURL {
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
			case "/DocumentReference/h1000":
				statusCode = http.StatusOK
				response = `{
					"resourceType": "DocumentReference",
					"id": "h1000",
					"meta": {
						"versionId": "7",
						"lastUpdated": "2019-08-01T22:42:13.477+00:00"
					},
					"status": "current",
					"type": {
						"text": "GENERATE_FROM_IMAGING_STUDY"
					},
					"subject": {
						"reference": "Patient/p1000"
					},
					"date": "2019-01-02T12:30:45+00:00",
					"author": [
						{
							"reference": "Practitioner/a1000"
						}
					],
					"description": "{\"description\":\"test-description\",\"creationDescription\":\"test-pipe\",\"bodySite\":\"hips\",\"dateOfImaging\":\"2017-07-15T15:20:25Z\"}",
					"content": [
						{
							"attachment": {
								"contentType": "application/test",
								"url": "www.storage.com/download/12345",
								"size": 1024000,
								"title": "test-title"
							}
						}
					]
				}`
			case "/DocumentReference/h2000":
				statusCode = http.StatusOK
				response = `{
					"resourceType": "DocumentReference",
					"id": "h2000",
					"meta": {
						"versionId": "2",
						"lastUpdated": "2019-08-02T16:03:16.481+00:00"
					},
					"status": "current",
					"type": {
						"text": "FROM_DEPTHVISOR_RECORDING"
					},
					"subject": {
						"reference": "Patient/p1000"
					},
					"date": "2019-01-02T12:30:45+00:00",
					"author": [
						{
							"reference": "Practitioner/a1000"
						}
					],
					"description": "{\"description\":\"test-description\",\"creationDescription\":\"test-pipe\",\"bodySite\":\"hips\",\"dateOfImaging\":\"2017-07-15T15:20:25Z\"}",
					"content": [
						{
							"attachment": {
								"contentType": "application/test",
								"url": "www.storage.com/download/12345",
								"size": 1024000,
								"title": "test-title"
							}
						}
					]
				}`
			case "/DocumentReference/h3000":
				statusCode = http.StatusNotFound
				response = `{
					"resourceType": "OperationOutcome",
					"id": "73f97942-f6da-4f02-ac81-2b9bc8be9fcf",
					"issue": [
						{
							"severity": "error",
							"code": "not-found",
							"diagnostics": "Resource type 'DocumentReference' with id 'h3000' couldn't be found."
						}
					]
				}`
			case "/DocumentReference?subject=p1000":
				statusCode = http.StatusOK
				response = `{
					"resourceType": "Bundle",
					"id": "f919522a-cd89-4e81-952d-e24037661579",
					"meta": {
						"lastUpdated": "2019-08-12T15:00:03.3998584+00:00"
					},
					"type": "searchset",
					"link": [
						{
							"relation": "next",
							"url": "http://{baseurl}/DocumentReference?ct=12345"
						},
						{
							"relation": "self",
							"url": "http://{baseurl}/DocumentReference?subject=p1000"
						}
					],
					"entry": [
						{
							"fullUrl": "http://{baseurl}/DocumentReference/h1000",
							"resource": {
								"resourceType": "DocumentReference",
								"id": "h1000",
								"meta": {
									"versionId": "7",
									"lastUpdated": "2019-08-01T22:42:13.477+00:00"
								},
								"status": "current",
								"type": {
									"text": "GENERATE_FROM_IMAGING_STUDY"
								},
								"subject": {
									"reference": "Patient/p1000"
								},
								"date": "2019-01-02T12:30:45+00:00",
								"author": [
									{
										"reference": "Practitioner/a1000"
									}
								],
								"description": "{\"description\":\"test-description\",\"creationDescription\":\"test-pipe\",\"bodySite\":\"hips\",\"dateOfImaging\":\"2017-07-15T15:20:25Z\"}",
								"content": [
									{
										"attachment": {
											"contentType": "application/test",
											"url": "www.storage.com/download/12345",
											"size": 1024000,
											"title": "test-title"
										}
									}
								]
							},
							"search": {
								"mode": "match"
							}
						},
						{
							"fullUrl": "http://{baseurl}/DocumentReference/h2000",
							"resource": {
								"resourceType": "DocumentReference",
								"id": "h2000",
								"meta": {
									"versionId": "2",
									"lastUpdated": "2019-08-02T16:03:16.481+00:00"
								},
								"status": "current",
								"type": {
									"text": "FROM_DEPTHVISOR_RECORDING"
								},
								"subject": {
									"reference": "Patient/p1000"
								},
								"date": "2019-01-02T12:30:45+00:00",
								"author": [
									{
										"reference": "Practitioner/a1000"
									}
								],
								"description": "{\"description\":\"test-description\",\"creationDescription\":\"test-pipe\",\"bodySite\":\"hips\",\"dateOfImaging\":\"2017-07-15T15:20:25Z\"}",
								"content": [
									{
										"attachment": {
											"contentType": "application/test",
											"url": "www.storage.com/download/12345",
											"size": 1024000,
											"title": "test-title"
										}
									}
								]
							},
							"search": {
								"mode": "match"
							}
						}
					]
				}`
				response = strings.ReplaceAll(response, "{baseurl}", baseurl)

			case "/DocumentReference?subject=p3000":
				statusCode = http.StatusOK
				response = `{
					"resourceType": "Bundle",
					"id": "0d9abdd0-137c-4715-8999-75d27f6ce53c",
					"meta": {
						"lastUpdated": "2019-08-12T16:07:36.2884727+00:00"
					},
					"type": "searchset",
					"link": [
						{
							"relation": "self",
							"url": "http://{baseurl}/DocumentReference?subject=p3000"
						}
					]
				}`
				response = strings.ReplaceAll(response, "{baseurl}", baseurl)

			case "/DocumentReference?ct=12345", "/DocumentReference?subject=p1000&type:text=UPLOAD_EXISTING_MODEL":
				statusCode = http.StatusOK
				response = `{
					"resourceType": "Bundle",
					"id": "875ea98a-b682-4213-a2ed-c76a873d55f8",
					"meta": {
						"lastUpdated": "2019-08-12T16:03:35.4903774+00:00"
					},
					"type": "searchset",
					"link": [
						{
							"relation": "self",
							"url": "http://{baseurl}/DocumentReference"
						}
					],
					"entry": [
						{
							"fullUrl": "http://{baseurl}/DocumentReference/h4000",
							"resource": {
								"resourceType": "DocumentReference",
								"id": "h4000",
								"meta": {
									"versionId": "1",
									"lastUpdated": "2019-08-12T12:49:41.761+00:00"
								},
								"status": "current",
								"type": {
									"text": "UPLOAD_EXISTING_MODEL"
								},
								"subject": {
									"reference": "Patient/p1000"
								},
								"date": "2017-07-21T17:32:28+00:00",
								"author": [
									{
										"reference": "Practitioner/a1000"
									}
								],
								"description": "{\"description\":\"Malformed hip bones on an 8 year old child suffering from a birth defect\",\"creationDescription\":\"Created using bone pipelines with HU threshold of 750\",\"bodySite\":\"hips\",\"dateOfImaging\":\"2017-07-18T12:00:30Z\"}",
								"content": [
									{
										"attachment": {
											"contentType": "model/gltf-binary",
											"size": 2048000,
											"title": "Malformed hip bones"
										}
									}
								]
							},
							"search": {
								"mode": "match"
							}
						}
					]
				}`
				response = strings.ReplaceAll(response, "{baseurl}", baseurl)

			default:
				log.Fatalln("Url not handled:", rcvURL)
			}
		} else if r.Method == "PUT" {
			switch rcvURL, _ := url.QueryUnescape(r.URL.String()); rcvURL {
			case "/Patient/assume-bad-id":
				statusCode = http.StatusBadRequest
				response = `{
					"resourceType": "OperationOutcome",
					"id": "f351b0a7-d236-4df5-a907-415d184b3539",
					"issue": [
						{
							"severity": "error",
							"code": "invalid",
							"diagnostics": "Id in the URL must match id in the resource."
						}
					]
				}`
			case "/Patient/assume-new-id":
				statusCode = http.StatusCreated
				response = `{
					"resourceType": "Patient",
					"id": "p1",
					"meta": {
						"versionId": "1",
						"lastUpdated": "2019-08-12T16:45:22.836+00:00"
					},
					"name": [
						{
							"text": "New Guy",
							"family": "Guy",
							"given": [
								"New"
							],
							"prefix": [
								"Mr"
							]
						}
					],
					"gender": "male",
					"birthDate": "1990-10-10"
				}`
			case "/Patient/assume-update-id":
				statusCode = http.StatusOK
				response = `{
					"resourceType": "Patient",
					"id": "p1",
					"meta": {
						"versionId": "2",
						"lastUpdated": "2019-08-12T16:45:22.836+00:00"
					},
					"name": [
						{
							"text": "New Guy",
							"family": "Guy",
							"given": [
								"New"
							],
							"prefix": [
								"Mr"
							]
						}
					],
					"gender": "male",
					"birthDate": "1990-10-10"
				}`
			case "/Practitioner/assume-bad-id":
				statusCode = http.StatusBadRequest
				response = `{
					"resourceType": "OperationOutcome",
					"id": "f351b0a7-d236-4df5-a907-415d184b3539",
					"issue": [
						{
							"severity": "error",
							"code": "invalid",
							"diagnostics": "Id in the URL must match id in the resource."
						}
					]
				}`
			case "/Practitioner/assume-new-id":
				statusCode = http.StatusCreated
				response = `{
					"resourceType": "Practitioner",
					"id": "p1",
					"meta": {
						"versionId": "1",
						"lastUpdated": "2019-08-12T16:45:22.836+00:00"
					},
					"name": [
						{
							"text": "New Guy",
							"family": "Guy",
							"given": [
								"New"
							],
							"prefix": [
								"Mr"
							]
						}
					]
				}`
			case "/Practitioner/assume-update-id":
				statusCode = http.StatusOK
				response = `{
					"resourceType": "Practitioner",
					"id": "p1",
					"meta": {
						"versionId": "2",
						"lastUpdated": "2019-08-12T16:45:22.836+00:00"
					},
					"name": [
						{
							"text": "New Guy",
							"family": "Guy",
							"given": [
								"New"
							],
							"prefix": [
								"Mr"
							]
						}
					]
				}`

			default:
				log.Fatalln("Url not handled:", rcvURL)
			}
		}

		w.WriteHeader(statusCode)
		fmt.Fprintf(w, response)
	}))

	l, _ := net.Listen("tcp", baseurl)
	ts.Listener = l
	ts.Start()

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

func TestHologramHidGet(t *testing.T) {
	type test struct {
		wantStatus int
		wantBody   Hologram
		wantErr    Error
		inUrl      string
		inMethod   string
	}

	tests := map[string]test{
		"found_hologram": {
			inUrl:      "/api/v1/holograms/h1000",
			inMethod:   http.MethodGet,
			wantStatus: 200,
			wantBody: Hologram{
				Hid:                 "h1000",
				Title:               "test-title",
				Description:         "test-description",
				ContentType:         "application/test",
				FileSizeInKb:        1000,
				BodySite:            "hips",
				DateOfImaging:       returnTime("2017-07-15T15:20:25Z"),
				CreationDate:        returnTime("2019-01-02T12:30:45Z"),
				CreationMode:        "GENERATE_FROM_IMAGING_STUDY",
				CreationDescription: "test-pipe",
				Aid:                 "a1000",
				Pid:                 "p1000",
			},
		},
		"missing_hologram": {
			inUrl:      "/api/v1/holograms/h3000",
			inMethod:   http.MethodGet,
			wantStatus: 404,
			wantErr: Error{
				ErrorCode:    "404",
				ErrorMessage: `id 'h3000' cannot be found`,
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

			if (tc.wantBody != Hologram{}) {
				var hologramData Hologram
				err := json.Unmarshal(w.Body.Bytes(), &hologramData)
				if err != nil {
					t.Fatalf("Unmarshal Hologram error: %s", err.Error())
				}
				diff = cmp.Diff(tc.wantBody, hologramData)
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

func TestMultipleHologramsGet(t *testing.T) {
	type test struct {
		wantStatus int
		wantBody   map[string][]Hologram
		wantErr    Error
		inUrl      string
		inMethod   string
	}

	tests := map[string]test{
		"no_pids_no_hids_used": {
			inUrl:      "/api/v1/holograms",
			inMethod:   http.MethodGet,
			wantStatus: 400,
			wantErr: Error{
				ErrorCode:    "400",
				ErrorMessage: "No hids or pids were provided for this query",
			},
		},
		"both_pids_and_hids_used": {
			inUrl:      "/api/v1/holograms?hids=h1000&pids=p1000",
			inMethod:   http.MethodGet,
			wantStatus: 400,
			wantErr: Error{
				ErrorCode:    "400",
				ErrorMessage: "Use either pid or hid, not both",
			},
		},
		"query_by_hid": {
			inUrl:      "/api/v1/holograms?hids=h1000,h3000",
			inMethod:   http.MethodGet,
			wantStatus: 200,
			wantBody: map[string][]Hologram{
				"h1000": []Hologram{
					Hologram{
						Hid:                 "h1000",
						Title:               "test-title",
						Description:         "test-description",
						ContentType:         "application/test",
						FileSizeInKb:        1000,
						BodySite:            "hips",
						DateOfImaging:       returnTime("2017-07-15T15:20:25Z"),
						CreationDate:        returnTime("2019-01-02T12:30:45Z"),
						CreationMode:        "GENERATE_FROM_IMAGING_STUDY",
						CreationDescription: "test-pipe",
						Aid:                 "a1000",
						Pid:                 "p1000",
					},
				},
				"h3000": []Hologram{},
			},
		},
		"query_by_pid": {
			inUrl:      "/api/v1/holograms?pids=p1000,p3000",
			inMethod:   http.MethodGet,
			wantStatus: 200,
			wantBody: map[string][]Hologram{
				"p1000": []Hologram{
					Hologram{
						Hid:                 "h1000",
						Title:               "test-title",
						Description:         "test-description",
						ContentType:         "application/test",
						FileSizeInKb:        1000,
						BodySite:            "hips",
						DateOfImaging:       returnTime("2017-07-15T15:20:25Z"),
						CreationDate:        returnTime("2019-01-02T12:30:45Z"),
						CreationMode:        "GENERATE_FROM_IMAGING_STUDY",
						CreationDescription: "test-pipe",
						Aid:                 "a1000",
						Pid:                 "p1000",
					},
					Hologram{
						Hid:                 "h2000",
						Title:               "test-title",
						Description:         "test-description",
						ContentType:         "application/test",
						FileSizeInKb:        1000,
						BodySite:            "hips",
						DateOfImaging:       returnTime("2017-07-15T15:20:25Z"),
						CreationDate:        returnTime("2019-01-02T12:30:45Z"),
						CreationMode:        "FROM_DEPTHVISOR_RECORDING",
						CreationDescription: "test-pipe",
						Aid:                 "a1000",
						Pid:                 "p1000",
					},
					Hologram{
						Hid:                 "h4000",
						Title:               "Malformed hip bones",
						Description:         "Malformed hip bones on an 8 year old child suffering from a birth defect",
						ContentType:         "model/gltf-binary",
						FileSizeInKb:        2000,
						BodySite:            "hips",
						DateOfImaging:       returnTime("2017-07-18T12:00:30Z"),
						CreationDate:        returnTime("2017-07-21T17:32:28Z"),
						CreationMode:        "UPLOAD_EXISTING_MODEL",
						CreationDescription: "Created using bone pipelines with HU threshold of 750",
						Aid:                 "a1000",
						Pid:                 "p1000",
					},
				},
				"p3000": []Hologram{},
			},
		},
		"query_pid_and_creationmode": {
			inUrl:      "/api/v1/holograms?pids=p1000&creationmode=UPLOAD_EXISTING_MODEL",
			inMethod:   http.MethodGet,
			wantStatus: 200,
			wantBody: map[string][]Hologram{
				"p1000": []Hologram{
					Hologram{
						Hid:                 "h4000",
						Title:               "Malformed hip bones",
						Description:         "Malformed hip bones on an 8 year old child suffering from a birth defect",
						ContentType:         "model/gltf-binary",
						FileSizeInKb:        2000,
						BodySite:            "hips",
						DateOfImaging:       returnTime("2017-07-18T12:00:30Z"),
						CreationDate:        returnTime("2017-07-21T17:32:28Z"),
						CreationMode:        "UPLOAD_EXISTING_MODEL",
						CreationDescription: "Created using bone pipelines with HU threshold of 750",
						Aid:                 "a1000",
						Pid:                 "p1000",
					},
				},
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
				var hologramData map[string][]Hologram
				err := json.Unmarshal(w.Body.Bytes(), &hologramData)
				if err != nil {
					t.Fatalf("Unmarshal Patient error: %s", err.Error())
				}
				diff = cmp.Diff(tc.wantBody, hologramData)
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

func TestPatientsPut(t *testing.T) {
	type test struct {
		wantStatus int
		wantBody   Patient
		wantErr    Error
		inUrl      string
		inMethod   string
		inHeader   map[string]string
		inBody     string
	}

	tests := map[string]test{
		"no_content_type_header": {
			inUrl:      "/api/v1/patients/assume-new-id",
			inMethod:   http.MethodPut,
			wantStatus: 400,
			wantErr: Error{
				ErrorCode:    "400",
				ErrorMessage: "Expected Content-Type: 'application/json', got ''",
			},
		},
		"put_patient_new": {
			inUrl:    "/api/v1/patients/assume-new-id",
			inMethod: http.MethodPut,
			inHeader: map[string]string{
				"Content-Type": "application/json",
			},
			inBody: `{
				"pid": "assume-new-id",
				"name": {
					"title": "Mr",
					"given": "New",
					"family": "Guy",
					"full": "New Guy"
				},
				"gender": "male",
				"birthDate": "1990-10-10"
			}`,
			wantStatus: 201,
			wantBody: Patient{
				Pid: "assume-new-id",
				Name: &PersonName{
					Title:  "Mr",
					Given:  "New",
					Family: "Guy",
					Full:   "New Guy",
				},
				Gender:    "male",
				BirthDate: "1990-10-10",
			},
		},
		"put_patient_update": {
			inUrl:    "/api/v1/patients/assume-update-id",
			inMethod: http.MethodPut,
			inHeader: map[string]string{
				"Content-Type": "application/json",
			},
			inBody: `{
				"pid": "assume-update-id",
				"name": {
					"title": "Mr",
					"given": "New",
					"family": "Guy",
					"full": "New Guy"
				},
				"gender": "male",
				"birthDate": "1990-10-10"
			}`,
			wantStatus: 200,
			wantBody: Patient{
				Pid: "assume-update-id",
				Name: &PersonName{
					Title:  "Mr",
					Given:  "New",
					Family: "Guy",
					Full:   "New Guy",
				},
				Gender:    "male",
				BirthDate: "1990-10-10",
			},
		},
		"put_patient_bad": {
			inUrl:    "/api/v1/patients/assume-bad-id",
			inMethod: http.MethodPut,
			inHeader: map[string]string{
				"Content-Type": "application/json",
			},
			inBody: `{
				"pid": "assume-mismatch-id",
				"name": {
					"title": "Mr",
					"given": "New",
					"family": "Guy",
					"full": "New Guy"
				},
				"gender": "male",
				"birthDate": "1990-10-10"
			}`,
			wantStatus: 400,
			wantErr: Error{
				ErrorCode:    "400",
				ErrorMessage: `pid in param and body do not match`,
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
			req, _ := http.NewRequest(tc.inMethod, tc.inUrl, bytes.NewBufferString(tc.inBody))
			for header, value := range tc.inHeader {
				req.Header.Set(header, value)
			}
			w := httptest.NewRecorder()
			router.ServeHTTP(w, req)

			if tc.wantStatus != w.Code {
				t.Fatalf("Error return code: Want %d, got %d. Body: %s", tc.wantStatus, w.Code, w.Body.String())
			}

			if (tc.wantBody != Patient{}) {
				var patientData Patient
				err := json.Unmarshal(w.Body.Bytes(), &patientData)
				if err != nil {
					fmt.Println(w.Body.String())
					t.Fatalf("Unmarshal Patient error: %s", err.Error())
				}
				diff = cmp.Diff(tc.wantBody, patientData)
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

func TestAuthorsPut(t *testing.T) {
	type test struct {
		wantStatus int
		wantBody   Author
		wantErr    Error
		inUrl      string
		inMethod   string
		inHeader   map[string]string
		inBody     string
	}

	tests := map[string]test{
		"no_content_type_header": {
			inUrl:      "/api/v1/authors/assume-new-id",
			inMethod:   http.MethodPut,
			wantStatus: 400,
			wantErr: Error{
				ErrorCode:    "400",
				ErrorMessage: "Expected Content-Type: 'application/json', got ''",
			},
		},
		"put_author_new": {
			inUrl:    "/api/v1/authors/assume-new-id",
			inMethod: http.MethodPut,
			inHeader: map[string]string{
				"Content-Type": "application/json",
			},
			inBody: `{
				"aid": "assume-new-id",
				"name": {
					"title": "Mr",
					"given": "New",
					"family": "Guy",
					"full": "New Guy"
				}
			}`,
			wantStatus: 201,
			wantBody: Author{
				Aid: "assume-new-id",
				Name: &PersonName{
					Title:  "Mr",
					Given:  "New",
					Family: "Guy",
					Full:   "New Guy",
				},
			},
		},
		"put_author_update": {
			inUrl:    "/api/v1/authors/assume-update-id",
			inMethod: http.MethodPut,
			inHeader: map[string]string{
				"Content-Type": "application/json",
			},
			inBody: `{
				"aid": "assume-update-id",
				"name": {
					"title": "Mr",
					"given": "New",
					"family": "Guy",
					"full": "New Guy"
				}
			}`,
			wantStatus: 200,
			wantBody: Author{
				Aid: "assume-update-id",
				Name: &PersonName{
					Title:  "Mr",
					Given:  "New",
					Family: "Guy",
					Full:   "New Guy",
				},
			},
		},
		"put_author_bad": {
			inUrl:    "/api/v1/authors/assume-bad-id",
			inMethod: http.MethodPut,
			inHeader: map[string]string{
				"Content-Type": "application/json",
			},
			inBody: `{
				"aid": "assume-mismatch-id",
				"name": {
					"title": "Mr",
					"given": "New",
					"family": "Guy",
					"full": "New Guy"
				}
			}`,
			wantStatus: 400,
			wantErr: Error{
				ErrorCode:    "400",
				ErrorMessage: `aid in param and body do not match`,
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
			req, _ := http.NewRequest(tc.inMethod, tc.inUrl, bytes.NewBufferString(tc.inBody))
			for header, value := range tc.inHeader {
				req.Header.Set(header, value)
			}
			w := httptest.NewRecorder()
			router.ServeHTTP(w, req)

			if tc.wantStatus != w.Code {
				t.Fatalf("Error return code: Want %d, got %d. Body: %s", tc.wantStatus, w.Code, w.Body.String())
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
