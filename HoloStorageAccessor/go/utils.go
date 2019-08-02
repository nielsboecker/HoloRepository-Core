package openapi

import (
	"encoding/json"
	"errors"
	"io/ioutil"
	"log"
	"net/url"
	"path"
	"strings"
)

type HologramQueryDetails struct {
	IDs          []string
	Mode         string
	CreationMode string
}

func VerifyHologramQuery(hid, pid, creationMode string) (HologramQueryDetails, error) {
	var details HologramQueryDetails
	if hid != "" && pid != "" {
		return HologramQueryDetails{}, errors.New("Use either pid or hid, not both")
	} else if hid != "" {
		details.IDs = ParseQueryIDs(hid)
		details.Mode = "hologram"
	} else if pid != "" {
		details.IDs = ParseQueryIDs(pid)
		details.Mode = "patient"
	}

	// Checks for creationmode usage
	switch creationMode {
	case "":
	case "GENERATE_FROM_IMAGING_STUDY", "UPLOAD_EXISTING_MODEL", "FROM_DEPTHVISOR_RECORDING":
		details.CreationMode = creationMode
	default:
		return HologramQueryDetails{}, errors.New("Invalid value used in creationmode")
	}

	return details, nil
}

// ParseQueryIDs - parse queries for ids sent via HTTP
func ParseQueryIDs(query string) []string {
	ids := strings.Split(query, ",")
	if len(ids) > 1 && ids[len(ids)-1] == "" {
		ids = ids[:len(ids)-1]
	}
	// Remove duplicates
	var final_ids []string
	tempDict := make(map[string]bool)
	for _, id := range ids {
		_, present := tempDict[id]
		if !present {
			tempDict[id] = true
			final_ids = append(final_ids, id)
		}
	}
	return final_ids
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
