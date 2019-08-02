package openapi

import (
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
		result.err = errors.New("Unsupported httpMethod: " + method)
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
