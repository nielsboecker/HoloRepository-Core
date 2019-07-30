package openapi

import (
	"log"
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
	url, err := url.Parse(baseurl)
	if err != nil {
		log.Fatal(err)
		return "", err
	}
	url.Path = path.Join(url.Path, pathComponent)
	return url.String(), nil
}

// func FHIRRestCall(baseurl string, data FHIRRequestData) (*Response, error) {
// 	url.Path = path.Join(url.Path)
// 	client := &http.Client{}

// 	req, err := http.NewRequest(
// 		data.HTTPMethod,
// 		"https://my-json-server.typicode.com/typicode/demo/posts",
// 		strings.NewReader(body)
// 	)
// 	req.Header.Add("Content-Type", "application/fhir+json")
// }
