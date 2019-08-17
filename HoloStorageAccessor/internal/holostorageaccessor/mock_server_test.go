package holostorageaccessor

import (
	"fmt"
	"log"
	"net"
	"net/http"
	"net/http/httptest"
	"net/url"
	"strings"
)

// This creates a test server that mocks the FHIR server responses
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
