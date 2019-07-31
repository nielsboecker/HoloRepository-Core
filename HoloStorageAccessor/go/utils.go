package openapi

import (
	"encoding/json"
	"io/ioutil"
	"log"
	"net/http"
	"net/url"
	"path"
	"strings"
)

type FHIRRequestData struct {
	HTTPMethod       string
	ResourcePathComp string
	Body             string
}

// ParseQueryIDs - parse queries for ids sent via HTTP
func ParseQueryIDs(query string) []string {
	ids := strings.Split(query, ",")
	if len(ids) > 1 && ids[len(ids)-1] == "" {
		ids = ids[:len(ids)-1]
	}
	return ids
}

func ConstructURL(baseurl string, pathComponent string) (string, error) {
	fhirURL, err := url.Parse(baseurl)
	if err != nil {
		log.Fatal(err)
		return "", err
	}
	fhirURL.Path = path.Join(fhirURL.Path, pathComponent)
	return fhirURL.String(), nil
}

func FHIRRestCall(baseurl string, data FHIRRequestData) ([]byte, error) {
	fhirURL, _ := ConstructURL(baseurl, data.ResourcePathComp)
	client := &http.Client{}

	req, err := http.NewRequest(
		data.HTTPMethod,
		fhirURL,
		strings.NewReader(data.Body))

	if err != nil {
		return []byte{}, err
	}
	req.Header.Add("Content-Type", "application/fhir+json")

	resp, err := client.Do(req)

	if err != nil {
		return []byte{}, err
	}
	defer resp.Body.Close()
	body, err := ioutil.ReadAll(resp.Body)

	return body, nil
}

func LoadConfiguration(confFile string, config *AccessorConfig) error {
	configfile, err := ioutil.ReadFile(confFile)
	if err != nil {
		return err
	}

	err = json.Unmarshal([]byte(configfile), config)
	if err != nil {
		return err
	}

	return nil
}

func SearchAuthors(aids []string) (map[string]Author, error) {
	var result map[string]Author
	var tempAuthor PractitionerFHIR

	result = make(map[string]Author)

	for _, aid := range aids {
		reqData := FHIRRequestData{HTTPMethod: http.MethodGet, ResourcePathComp: "Practitioner/" + aid}
		body, err := FHIRRestCall(accessorConfig.FhirURL, reqData)
		if err != nil {
			return make(map[string]Author), err
		}
		err = json.Unmarshal(body, &tempAuthor)
		if err != nil {
			return make(map[string]Author), err
		}
		if tempAuthor.ID != aid {
			result[aid] = Author{}
		} else {
			result[aid] = tempAuthor.ToAPISpec()
		}
	}

	return result, nil
}
