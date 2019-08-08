package holostorageaccessor

import (
	"encoding/json"
	"errors"
	"fmt"
	"net/url"
	"os"
	"path"
	"strconv"
	"strings"
	"time"
)

type HologramQueryDetails struct {
	IDs          []string
	Mode         string
	CreationMode string
}

type HologramPostInput struct {
	Hologram Hologram
	Author   Author
	Patient  Patient
}

func ParseHologramUploadPostInput(formData url.Values) (HologramPostInput, error) {
	var authorData Author
	var patientData Patient
	var hologramData Hologram

	for key, _ := range formData {
		switch key {
		case "patient":
			err := json.Unmarshal([]byte(formData.Get(key)), &patientData)
			if err != nil {
				return HologramPostInput{}, errors.New("Unable to parse patient data")
			}
			if patientData.Pid == "" {
				return HologramPostInput{}, errors.New("Patient ID is required")
			}
			hologramData.Pid = patientData.Pid
		case "author":
			err := json.Unmarshal([]byte(formData.Get(key)), &authorData)
			if err != nil {
				return HologramPostInput{}, errors.New("Unable to parse author data")
			}
			if authorData.Aid == "" {
				return HologramPostInput{}, errors.New("Author ID is required")
			}
			hologramData.Aid = authorData.Aid
		case "creationDate":
			creationDate, err := time.Parse(time.RFC3339, formData.Get(key))
			if err != nil {
				return HologramPostInput{}, fmt.Errorf("Key %s='%s' does not conform to RFC3339 standards", key, formData.Get(key))
			}
			hologramData.CreationDate = &creationDate
		case "dateOfImaging":
			dateOfImaging, err := time.Parse(time.RFC3339, formData.Get(key))
			if err != nil {
				return HologramPostInput{}, fmt.Errorf("Key %s='%s' does not conform to RFC3339 standards", key, formData.Get(key))
			}
			hologramData.DateOfImaging = &dateOfImaging
		case "title":
			hologramData.Title = formData.Get(key)
		case "description":
			hologramData.Description = formData.Get(key)
		case "contentType":
			hologramData.ContentType = formData.Get(key)
		case "fileSizeInKB":
			fileSize, err := strconv.ParseUint(formData.Get(key), 10, 32)
			if err != nil {
				return HologramPostInput{}, errors.New(key + " is not a valid filesize")
			}
			hologramData.FileSizeInKb = uint32(fileSize)
		case "bodySite":
			hologramData.BodySite = formData.Get(key)
		case "creationMode":
			hologramData.CreationMode = formData.Get(key)
		case "creationDescription":
			hologramData.CreationDescription = formData.Get(key)
		}
	}

	result := HologramPostInput{Author: authorData, Patient: patientData, Hologram: hologramData}
	return result, nil
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
	var finalIDs []string
	tempDict := make(map[string]bool)
	for _, id := range ids {
		_, present := tempDict[id]
		if !present {
			tempDict[id] = true
			finalIDs = append(finalIDs, id)
		}
	}
	return finalIDs
}

func ConstructURL(baseurl string, pathComponent string) (string, error) {
	fhirURL, _ := url.Parse(baseurl)
	fhirURL.Path = path.Join(fhirURL.Path, pathComponent)
	return fhirURL.String(), nil
}

func LoadConfiguration(config *AccessorConfig) error {
	for _, config := range []string{"AZURE_STORAGE_ACCOUNT", "AZURE_STORAGE_ACCESS_KEY", "ACCESSOR_FHIR_URL"} {
		if os.Getenv(config) == "" {
			return fmt.Errorf("Environment config field '%s' is not set", config)
		}
	}

	config.BlobStorageName = strings.TrimSpace(os.Getenv("AZURE_STORAGE_ACCOUNT"))
	config.BlobStorageKey = strings.TrimSpace(os.Getenv("AZURE_STORAGE_ACCESS_KEY"))
	config.FhirURL = strings.TrimSpace(os.Getenv("ACCESSOR_FHIR_URL"))

	_, err := url.ParseRequestURI(config.FhirURL)
	if err != nil {
		return fmt.Errorf("Error with ACCESSOR_FHIR_URL: %s", err.Error())
	}

	err = InitialiseBlobStorage(config.BlobStorageName, config.BlobStorageKey)
	if err != nil {
		return fmt.Errorf("Error with BlobStorage Init: %s", err.Error())
	}

	return nil
}
