package holostorageaccessor

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"net/http/httptest"
	"os"
	"testing"

	"github.com/gin-gonic/gin"
	"github.com/google/go-cmp/cmp"
)

var router *gin.Engine

// TestMain() used to setup a mock fhir server which will be used by all tests
// ref: https://golang.org/pkg/testing/#hdr-Main
func TestMain(m *testing.M) {
	ts := setupTestServer()
	defer ts.Close()
	router = NewRouter(AccessorConfig{FhirURL: ts.URL})
	os.Exit(m.Run())
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
