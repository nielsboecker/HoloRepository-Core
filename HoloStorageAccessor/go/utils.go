package openapi

import (
	"encoding/json"
	"io/ioutil"
	"log"
	"net/url"
	"path"
	"strings"
)

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
