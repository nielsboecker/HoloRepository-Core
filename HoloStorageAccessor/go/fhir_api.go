package openapi

import (
	"io/ioutil"
	"net/http"
	"strings"
)

type FHIRRequest struct {
	httpMethod string
	url        string
	qid        string
	body       string
}

type FHIRResult struct {
	err      error
	qid      string
	response []byte
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

	result.response = body
	c <- result
}
