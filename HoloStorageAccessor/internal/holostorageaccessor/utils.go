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
				return HologramPostInput{}, fmt.Errorf("Unable to parse patient data: %s", err.Error())
			}
			if patientData.Pid == "" {
				return HologramPostInput{}, errors.New("Patient ID is required")
			}
			hologramData.Pid = patientData.Pid
		case "author":
			err := json.Unmarshal([]byte(formData.Get(key)), &authorData)
			if err != nil {
				return HologramPostInput{}, fmt.Errorf("Unable to parse author data: %s", err.Error())
			}
			if authorData.Aid == "" {
				return HologramPostInput{}, errors.New("Author ID is required")
			}
			hologramData.Aid = authorData.Aid
		case "creationDate":
			dateString := formData.Get(key)
			if dateString != "" {
				creationDate, err := time.Parse(time.RFC3339, dateString)
				if err != nil {
					return HologramPostInput{}, fmt.Errorf("Key %s='%s' does not conform to RFC3339 standards", key, formData.Get(key))
				}
				hologramData.CreationDate = &creationDate
			}
		case "dateOfImaging":
			dateString := formData.Get(key)
			if dateString != "" {
				dateOfImaging, err := time.Parse(time.RFC3339, dateString)
				if err != nil {
					return HologramPostInput{}, fmt.Errorf("Key %s='%s' does not conform to RFC3339 standards", key, formData.Get(key))
				}
				hologramData.DateOfImaging = &dateOfImaging
			}
		case "title":
			hologramData.Title = formData.Get(key)
		case "description":
			hologramData.Description = formData.Get(key)
		case "contentType":
			hologramData.ContentType = formData.Get(key)
		case "fileSizeInKb":
			fileSize, err := strconv.ParseUint(formData.Get(key), 10, 32)
			if err != nil {
				return HologramPostInput{}, fmt.Errorf("Key %s='%s' is not a valid filesize value", key, formData.Get(key))
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
	} else if hid == "" && pid == "" {
		return HologramQueryDetails{}, errors.New("No hids or pids were provided for this query")
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
		return HologramQueryDetails{}, errors.New(`Invalid value used in creationmode. Expecting: GENERATE_FROM_IMAGING_STUDY, UPLOAD_EXISTING_MODEL, FROM_DEPTHVISOR_RECORDING`)
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

func LoadConfiguration(accConfig *AccessorConfig) error {
	for _, config := range []string{"AZURE_STORAGE_ACCOUNT", "AZURE_STORAGE_ACCESS_KEY", "ACCESSOR_FHIR_URL", "ENABLE_CORS"} {
		if os.Getenv(config) == "" {
			return fmt.Errorf("Environment config field '%s' is not set", config)
		}
	}

	accConfig.BlobStorageName = strings.TrimSpace(os.Getenv("AZURE_STORAGE_ACCOUNT"))
	accConfig.BlobStorageKey = strings.TrimSpace(os.Getenv("AZURE_STORAGE_ACCESS_KEY"))
	accConfig.FhirURL = strings.TrimSpace(os.Getenv("ACCESSOR_FHIR_URL"))

	enableCORS, err := strconv.ParseBool(strings.TrimSpace(os.Getenv("ENABLE_CORS")))
	if err != nil {
		return fmt.Errorf("ENABLE_CORS error: %s", err.Error())
	}
	accConfig.EnableCORS = enableCORS

	_, err = url.ParseRequestURI(accConfig.FhirURL)
	if err != nil {
		return fmt.Errorf("ACCESSOR_FHIR_URL error: %s", err.Error())
	}

	return nil
}
