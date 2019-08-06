/*
 * HoloStorage Accessor API
 *
 * API to access holograms and metadata from HoloStorage
 *
 * API version: 1.0.0
 */

package openapi

import (
	"bytes"
	"encoding/json"
	"net/http"
	"strings"

	"github.com/gin-gonic/gin"
)

// AuthorsAidGet - Get a single author metadata in HoloStorage
func AuthorsAidGet(c *gin.Context) {
	id := c.Param("aid")
	fhirURL, _ := ConstructURL(accessorConfig.FhirURL, "Practitioner/"+id)
	result := SingleFHIRQuery(FHIRRequest{httpMethod: "GET", qid: id, url: fhirURL})

	if result.err != nil {
		c.JSON(http.StatusInternalServerError, Error{ErrorCode: "500", ErrorMessage: result.err.Error()})
		return
	} else if result.statusCode == 404 || result.statusCode == 410 {
		errMsg := "id '" + id + "' cannot be found"
		c.JSON(http.StatusNotFound, Error{ErrorCode: "404", ErrorMessage: errMsg})
		return
	}
	var data PractitionerFHIR
	err := json.Unmarshal(result.response, &data)
	if err != nil {
		c.JSON(http.StatusInternalServerError, err.Error())
		return
	}
	c.JSON(http.StatusOK, data.ToAPISpec())
}

// AuthorsAidPut - Add or update author information
func AuthorsAidPut(c *gin.Context) {
	contentType := c.Request.Header.Get("Content-Type")
	if contentType != "application/json" {
		c.JSON(http.StatusBadRequest, Error{ErrorCode: "400", ErrorMessage: "Expected Content-Type: 'application/json', got '" + contentType + "'"})
		return
	}

	var data Author
	decoder := json.NewDecoder(c.Request.Body)
	err := decoder.Decode(&data)
	if err != nil {
		c.JSON(http.StatusBadRequest, Error{ErrorCode: "400", ErrorMessage: err.Error()})
		return
	}

	id := c.Param("aid")
	if data.Aid != id {
		c.JSON(http.StatusBadRequest, Error{ErrorCode: "400", ErrorMessage: "aid in param and body do not match"})
		return
	}

	dataFhir := data.ToFHIR()
	jsonData, _ := json.Marshal(dataFhir)
	fhirURL, _ := ConstructURL(accessorConfig.FhirURL, "Practitioner/"+id)
	result := SingleFHIRQuery(FHIRRequest{httpMethod: "PUT", qid: id, url: fhirURL, body: string(jsonData)})
	if result.err != nil {
		c.JSON(http.StatusInternalServerError, Error{ErrorCode: "500", ErrorMessage: result.err.Error()})
		return
	}
	c.JSON(result.statusCode, dataFhir)
}

// AuthorsGet - Mass query for author metadata in HoloStorage
func AuthorsGet(c *gin.Context) {
	fhirRequests := make(map[string]FHIRRequest)
	ids := ParseQueryIDs(c.Query("aid"))

	for _, id := range ids {
		fhirURL, _ := ConstructURL(accessorConfig.FhirURL, "Practitioner/"+id)
		fhirRequests[id] = FHIRRequest{httpMethod: "GET", qid: id, url: fhirURL}
	}

	results := BatchFHIRQuery(fhirRequests)

	dataMap := make(map[string]Author)
	var emptyData Author
	for id, result := range results {
		if result.statusCode == 404 || result.statusCode == 410 {
			dataMap[id] = emptyData
		} else {
			var tempData PractitionerFHIR
			err := json.Unmarshal(result.response, &tempData)
			if err != nil {
				c.JSON(http.StatusInternalServerError, err.Error())
				return
			}
			dataMap[id] = tempData.ToAPISpec()
		}
	}

	c.JSON(http.StatusOK, dataMap)
}

// HologramsGet - Mass query for hologram metadata based on hologram ids
func HologramsGet(c *gin.Context) {
	hid := c.Query("hid")
	pid := c.Query("pid")
	creationMode := c.Query("creationmode")
	details, err := VerifyHologramQuery(hid, pid, creationMode)
	if err != nil {
		c.JSON(http.StatusBadRequest, Error{ErrorCode: "400", ErrorMessage: err.Error()})
		return
	}

	// Process requests
	fhirRequests := make(map[string]FHIRRequest)

	switch details.Mode {
	case "hologram":
		for _, id := range details.IDs {
			fhirURL, _ := ConstructURL(accessorConfig.FhirURL, "DocumentReference/"+id)
			fhirRequests[id] = FHIRRequest{httpMethod: "GET", qid: id, url: fhirURL}
		}
	case "patient":
		for _, id := range details.IDs {
			query := make(map[string]string)
			if creationMode != "" {
				query["type:text"] = creationMode
			}
			query["subject"] = id
			fhirURL, _ := ConstructURL(accessorConfig.FhirURL, "DocumentReference")
			fhirRequests[id] = FHIRRequest{httpMethod: "GET", qid: id, url: fhirURL, query: query}
		}
	}

	// Process queries to FHIR backend
	results := BatchFHIRQuery(fhirRequests)

	// Initialise blank results
	dataMap := make(map[string][]Hologram)
	for _, id := range details.IDs {
		dataMap[id] = []Hologram{}
	}

	switch details.Mode {
	case "hologram":
		for id, result := range results {
			if result.statusCode != 404 && result.statusCode != 410 {
				var tempData HologramDocumentReferenceFHIR
				err := json.Unmarshal(result.response, &tempData)
				if err != nil {
					c.JSON(http.StatusInternalServerError, err.Error())
					return
				}
				dataMap[id] = append(dataMap[id], tempData.ToAPISpec())
			}
		}
		c.JSON(http.StatusOK, dataMap)

	case "patient":
		type LinkFHIR struct {
			Relation string `json:"relation"`
			Url      string `json:"url"`
		}
		type EntryFHIR struct {
			Resource json.RawMessage `json:"resource"`
		}
		type BundleFHIR struct {
			Link  []LinkFHIR  `json:"link"`
			Entry []EntryFHIR `json:"entry"`
		}
		continueQuery := true
		for continueQuery {
			fhirRequests = make(map[string]FHIRRequest)
			for id, result := range results {
				var bundleResult BundleFHIR
				_ = json.Unmarshal(result.response, &bundleResult)
				for _, link := range bundleResult.Link {
					if link.Relation == "next" {
						fhirRequests[id] = FHIRRequest{httpMethod: "GET", url: link.Url, qid: id}
					}
				}
				for _, entry := range bundleResult.Entry {
					var tempData HologramDocumentReferenceFHIR
					_ = json.Unmarshal(entry.Resource, &tempData)
					dataMap[id] = append(dataMap[id], tempData.ToAPISpec())
				}
			}

			if len(fhirRequests) == 0 {
				continueQuery = false
			} else {
				results = BatchFHIRQuery(fhirRequests)
			}
		}
		c.JSON(http.StatusOK, dataMap)
	}
}

// HologramsHidDelete - Delete a hologram in HoloStorage
func HologramsHidDelete(c *gin.Context) {
	id := c.Param("hid")
	fhirURL, _ := ConstructURL(accessorConfig.FhirURL, "DocumentReference/"+id)
	result := SingleFHIRQuery(FHIRRequest{httpMethod: "GET", qid: id, url: fhirURL})

	if result.err != nil {
		c.JSON(http.StatusInternalServerError, Error{ErrorCode: "500", ErrorMessage: result.err.Error()})
		return
	} else if result.statusCode == 404 || result.statusCode == 410 {
		errMsg := "id '" + id + "' cannot be found"
		c.JSON(http.StatusNotFound, Error{ErrorCode: "404", ErrorMessage: errMsg})
		return
	}

	result = SingleFHIRQuery(FHIRRequest{httpMethod: "DELETE", qid: id, url: fhirURL})
	if result.err != nil {
		c.JSON(http.StatusInternalServerError, Error{ErrorCode: "500", ErrorMessage: result.err.Error()})
		return
	}

	// TODO: Blob storage deletion
	c.JSON(http.StatusOK, gin.H{"success": "Deleted hid '" + id + "'"})
}

// HologramsHidDownloadGet - Download holograms models based on the hologram id
func HologramsHidDownloadGet(c *gin.Context) {
	var id = c.Param("hid")
	var hologramFhir HologramDocumentReferenceFHIR
	err := GetSingleFHIRMetadata(accessorConfig.FhirURL, id, &hologramFhir)
	if err != nil {
		errArray := strings.SplitN(err.Error(), ":", 2)
		errCode, errMsg := errArray[0], errArray[1]
		if errCode == "404" {
			c.JSON(http.StatusNotFound, Error{ErrorCode: errCode, ErrorMessage: errMsg})
		} else {
			c.JSON(http.StatusInternalServerError, Error{ErrorCode: errCode, ErrorMessage: errMsg})
		}
		return
	}

	hologramAPISpec := hologramFhir.ToAPISpec()

	// TODO: Blob storage download
	var data bytes.Buffer

	data, err = DownloadHologramFromBlobStorage(id)
	if err != nil {
		c.JSON(http.StatusInternalServerError, Error{ErrorCode: "500", ErrorMessage: err.Error()})
		return
	}
	extraHeaders := map[string]string{
		"Content-Disposition": `attachment; filename="` + id + `.glb"`,
	}
	c.DataFromReader(http.StatusOK, int64(data.Len()), hologramAPISpec.ContentType, bytes.NewReader(data.Bytes()), extraHeaders)
}

// HologramsHidGet - Get a single hologram metadata based on the hologram id
func HologramsHidGet(c *gin.Context) {
	id := c.Param("hid")
	var data HologramDocumentReferenceFHIR
	err := GetSingleFHIRMetadata(accessorConfig.FhirURL, id, &data)
	if err != nil {
		errArray := strings.SplitN(err.Error(), ":", 2)
		errCode, errMsg := errArray[0], errArray[1]
		if errCode == "404" {
			c.JSON(http.StatusNotFound, Error{ErrorCode: errCode, ErrorMessage: errMsg})
		} else {
			c.JSON(http.StatusInternalServerError, Error{ErrorCode: errCode, ErrorMessage: errMsg})
		}
		return
	}
	c.JSON(http.StatusOK, data.ToAPISpec())
}

// HologramsPost - Upload hologram to HoloStorage
func HologramsPost(c *gin.Context) {
	contentType := c.Request.Header.Get("Content-Type")
	if !strings.HasPrefix(contentType, "multipart/form-data") {
		c.JSON(http.StatusBadRequest, Error{ErrorCode: "400", ErrorMessage: "Expected Content-Type: 'multipart/form-data', got '" + contentType + "'"})
		return
	}

	err := c.Request.ParseMultipartForm(32 << 20) // Reserve 32 MB for multipart data
	if err != nil {
		c.JSON(http.StatusInternalServerError, Error{ErrorCode: "500", ErrorMessage: "Unable to parse multipart/form"})
		return
	}
	postMetadata, err := ParseHologramUploadPostInput(c.Request.PostForm)
	if err != nil {
		c.JSON(http.StatusBadRequest, Error{ErrorCode: "400", ErrorMessage: err.Error()})
		return
	}
	hologramFile, err := c.FormFile("hologramFile")
	if err != nil {
		c.JSON(http.StatusInternalServerError, Error{ErrorCode: "500", ErrorMessage: err.Error()})
	}

	// TODO: Consider error handling for partial failures
	result := PutDataIntoFHIR(accessorConfig.FhirURL, postMetadata.Author)
	if result.err != nil {
		c.JSON(http.StatusInternalServerError, Error{ErrorCode: "500", ErrorMessage: result.err.Error()})
		return
	}
	result = PutDataIntoFHIR(accessorConfig.FhirURL, postMetadata.Author)
	if result.err != nil {
		c.JSON(http.StatusInternalServerError, Error{ErrorCode: "500", ErrorMessage: result.err.Error()})
		return
	}
	result = PostDataIntoFHIR(accessorConfig.FhirURL, postMetadata.Hologram)
	if result.err != nil {
		c.JSON(http.StatusInternalServerError, Error{ErrorCode: "500", ErrorMessage: result.err.Error()})
		return
	}

	var newHologram HologramDocumentReferenceFHIR
	_ = json.Unmarshal(result.response, &newHologram)
	newHologramAPISpec := newHologram.ToAPISpec()

	// TODO: Blob storage upload
	hologramFileIO, err := hologramFile.Open()
	if err != nil {
		c.JSON(http.StatusInternalServerError, Error{ErrorCode: "500", ErrorMessage: err.Error()})
	}

	err = UploadHologramToBlobStorage(newHologramAPISpec.Hid, hologramFileIO)
	if err != nil {
		c.JSON(http.StatusInternalServerError, Error{ErrorCode: "500", ErrorMessage: err.Error()})
	}

	c.JSON(http.StatusOK, newHologram.ToAPISpec())
}

// PatientsGet - Mass query for patients metadata in HoloStorage
func PatientsGet(c *gin.Context) {
	fhirRequests := make(map[string]FHIRRequest)
	ids := ParseQueryIDs(c.Query("pid"))

	for _, id := range ids {
		fhirURL, _ := ConstructURL(accessorConfig.FhirURL, "Patient/"+id)
		fhirRequests[id] = FHIRRequest{httpMethod: "GET", qid: id, url: fhirURL}
	}

	results := BatchFHIRQuery(fhirRequests)

	dataMap := make(map[string]Patient)
	var emptyData Patient
	for id, result := range results {
		if result.statusCode == 404 || result.statusCode == 410 {
			dataMap[id] = emptyData
		} else {
			var tempData PatientFHIR
			err := json.Unmarshal(result.response, &tempData)
			if err != nil {
				c.JSON(http.StatusInternalServerError, err.Error())
				return
			}
			dataMap[id] = tempData.ToAPISpec()
		}
	}

	c.JSON(http.StatusOK, dataMap)
}

// PatientsPidGet - Get a single patient metadata in HoloStorage
func PatientsPidGet(c *gin.Context) {
	id := c.Param("pid")
	fhirURL, _ := ConstructURL(accessorConfig.FhirURL, "Patient/"+id)
	result := SingleFHIRQuery(FHIRRequest{httpMethod: "GET", qid: id, url: fhirURL})

	if result.err != nil {
		c.JSON(http.StatusInternalServerError, Error{ErrorCode: "500", ErrorMessage: result.err.Error()})
		return
	} else if result.statusCode == 404 || result.statusCode == 410 {
		errMsg := "id '" + id + "' cannot be found"
		c.JSON(http.StatusNotFound, Error{ErrorCode: "404", ErrorMessage: errMsg})
		return
	}

	var data PatientFHIR
	err := json.Unmarshal(result.response, &data)
	if err != nil {
		c.JSON(http.StatusInternalServerError, err.Error())
		return
	}
	c.JSON(http.StatusOK, data.ToAPISpec())
}

// PatientsPidPut - Add or update basic patient information
func PatientsPidPut(c *gin.Context) {
	contentType := c.Request.Header.Get("Content-Type")
	if contentType != "application/json" {
		c.JSON(http.StatusBadRequest, Error{ErrorCode: "400", ErrorMessage: "Expected Content-Type: 'application/json', got '" + contentType + "'"})
		return
	}

	var data Patient
	id := c.Param("pid")

	decoder := json.NewDecoder(c.Request.Body)
	err := decoder.Decode(&data)
	if err != nil {
		c.JSON(http.StatusBadRequest, Error{ErrorCode: "400", ErrorMessage: err.Error()})
		return
	}

	if data.Pid != id {
		c.JSON(http.StatusBadRequest, Error{ErrorCode: "400", ErrorMessage: "pid in param and body do not match"})
		return
	}

	dataFhir := data.ToFHIR()
	jsonData, _ := json.Marshal(dataFhir)
	fhirURL, _ := ConstructURL(accessorConfig.FhirURL, "Patient/"+id)
	result := SingleFHIRQuery(FHIRRequest{httpMethod: "PUT", qid: id, url: fhirURL, body: string(jsonData)})
	if result.err != nil {
		c.JSON(http.StatusInternalServerError, Error{ErrorCode: "500", ErrorMessage: result.err.Error()})
		return
	}
	c.JSON(result.statusCode, dataFhir)
}
