package openapi

import (
	"encoding/json"
	"errors"
	"io/ioutil"
	"net/http"
	"strings"
)

type FHIRRequest struct {
	httpMethod string
	url        string
	qid        string
	body       string
	query      map[string]string
}

type FHIRResult struct {
	err        error
	statusCode int
	qid        string
	response   []byte
}

func SingleFHIRQuery(fhirReq FHIRRequest) FHIRResult {
	fhirChan := make(chan FHIRResult)
	defer close(fhirChan)
	go processFHIRQuery(fhirReq, fhirChan)
	return <-fhirChan
}

func BatchFHIRQuery(fhirRequests map[string]FHIRRequest) map[string]FHIRResult {
	var results map[string]FHIRResult
	results = make(map[string]FHIRResult)

	fhirChan := make(chan FHIRResult)
	defer close(fhirChan)

	for _, req := range fhirRequests {
		go processFHIRQuery(req, fhirChan)
	}

	for i := 0; i < len(fhirRequests); i++ {
		result := <-fhirChan
		results[result.qid] = result
	}

	return results
}

func processFHIRQuery(fhirReq FHIRRequest, c chan FHIRResult) {
	var req *http.Request
	result := FHIRResult{qid: fhirReq.qid, err: nil, response: nil}
	client := &http.Client{}

	switch method := fhirReq.httpMethod; method {
	case "GET", "DELETE":
		req, _ = http.NewRequest(fhirReq.httpMethod, fhirReq.url, nil)
	case "PUT", "POST":
		req, _ = http.NewRequest(fhirReq.httpMethod, fhirReq.url, strings.NewReader(fhirReq.body))
		req.Header.Add("Content-Type", "application/fhir+json")
	default:
		result.err = errors.New("Unsupported httpMethod: '" + method + "'")
		c <- result
		return
	}

	if fhirReq.query != nil {
		urlQuery := req.URL.Query()
		for queryKey, queryValue := range fhirReq.query {
			urlQuery.Add(queryKey, queryValue)
		}
		req.URL.RawQuery = urlQuery.Encode()
	}

	resp, err := client.Do(req)
	if err != nil {
		result.err = err
		c <- result
		return
	}
	defer resp.Body.Close()
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		result.err = err
		c <- result
		return
	}

	result.statusCode = resp.StatusCode
	result.response = body
	c <- result
}

func PutDataIntoFHIR(fhirBaseUrl string, fhirData interface{}) FHIRResult {
	var fhirRequest FHIRRequest
	var url string
	var jsonBody []byte

	switch data := fhirData.(type) {
	case Patient:
		dataFhir := data.ToFHIR()
		jsonBody, _ = json.Marshal(dataFhir)
		url, _ = ConstructURL(fhirBaseUrl, "Patient/"+data.Pid)
		fhirRequest = FHIRRequest{httpMethod: "PUT", qid: data.Pid, url: url, body: string(jsonBody)}
	case Author:
		dataFhir := data.ToFHIR()
		jsonBody, _ = json.Marshal(dataFhir)
		url, _ = ConstructURL(fhirBaseUrl, "Practitioner/"+data.Aid)
		fhirRequest = FHIRRequest{httpMethod: "PUT", qid: data.Aid, url: url, body: string(jsonBody)}
	default:
		return FHIRResult{err: errors.New("Unsupported datatype")}
	}

	return SingleFHIRQuery(fhirRequest)
}

func PostDataIntoFHIR(fhirBaseUrl string, fhirData interface{}) FHIRResult {
	var fhirRequest FHIRRequest
	var url string
	var jsonBody []byte

	switch data := fhirData.(type) {
	case Hologram:
		dataFhir := data.ToFHIR()
		jsonBody, _ = json.Marshal(dataFhir)
		url, _ = ConstructURL(fhirBaseUrl, "DocumentReference")
		fhirRequest = FHIRRequest{httpMethod: "POST", qid: "no-id", url: url, body: string(jsonBody)}
	default:
		return FHIRResult{err: errors.New("Unsupported datatype")}
	}

	return SingleFHIRQuery(fhirRequest)
}
