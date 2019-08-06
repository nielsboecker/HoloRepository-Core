package openapi

import (
	"encoding/json"
	"errors"
	"fmt"
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
	var id string
	var jsonBody []byte

	switch data := fhirData.(type) {
	case Patient:
		dataFhir := data.ToFHIR()
		jsonBody, _ = json.Marshal(dataFhir)
		id = data.Pid
		url, _ = ConstructURL(fhirBaseUrl, "Patient/"+id)
	case Author:
		dataFhir := data.ToFHIR()
		jsonBody, _ = json.Marshal(dataFhir)
		id = data.Aid
		url, _ = ConstructURL(fhirBaseUrl, "Practitioner/"+id)
	default:
		return FHIRResult{err: errors.New("Unsupported datatype")}
	}
	fhirRequest = FHIRRequest{httpMethod: "PUT", qid: id, url: url, body: string(jsonBody)}

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

func GetSingleFHIRMetadata(fhirBaseurl, id string, fhirType interface{}) error {
	var fhirURL string
	var err error

	switch fhirType := fhirType.(type) {
	case *HologramDocumentReferenceFHIR:
		fhirURL, _ = ConstructURL(fhirBaseurl, "DocumentReference/"+id)
	case *PatientFHIR:
		fhirURL, _ = ConstructURL(fhirBaseurl, "Patient/"+id)
	case *PractitionerFHIR:
		fhirURL, _ = ConstructURL(fhirBaseurl, "Practitioner/"+id)
	default:
		return fmt.Errorf("Unsupported fhirType struct: %T", fhirType)
	}

	result := SingleFHIRQuery(FHIRRequest{httpMethod: "GET", qid: id, url: fhirURL})
	if result.err != nil {
		return fmt.Errorf("500:%s", result.err.Error())
	} else if result.statusCode == 404 || result.statusCode == 410 {
		errMsg := "id '" + id + "' cannot be found"
		return fmt.Errorf("404:%s", errMsg)
	}

	switch fhirType := fhirType.(type) {
	case *HologramDocumentReferenceFHIR:
		err = json.Unmarshal(result.response, &fhirType)
	case *PatientFHIR:
		err = json.Unmarshal(result.response, &fhirType)
	case *PractitionerFHIR:
		err = json.Unmarshal(result.response, &fhirType)
	}

	if err != nil {
		return fmt.Errorf("500:%s", err.Error())
	}
	return nil
}
