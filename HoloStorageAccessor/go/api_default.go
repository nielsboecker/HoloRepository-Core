/*
 * HoloStorage Accessor API
 *
 * API to access holograms and metadata from HoloStorage
 *
 * API version: 1.0.0
 * Generated by: OpenAPI Generator (https://openapi-generator.tech)
 */

package openapi

import (
	"encoding/json"
	"fmt"
	"net/http"

	"github.com/gin-gonic/gin"
)

// AuthorsAidGet - Get a single author metadata in HoloStorage
func AuthorsAidGet(c *gin.Context) {
	aid := c.Param("aid")
	fhirURL, _ := ConstructURL(accessorConfig.FhirURL, "Practitioner/"+aid)
	result := SingleFHIRQuery(FHIRRequest{httpMethod: http.MethodGet, qid: aid, url: fhirURL})

	if result.err != nil {
		c.JSON(http.StatusInternalServerError, Error{ErrorCode: "500", ErrorMessage: result.err.Error()})
		return
	}
	var author PractitionerFHIR
	err := json.Unmarshal(result.response, &author)
	if err != nil {
		c.JSON(http.StatusInternalServerError, err.Error())
		return
	}
	if author.ID != aid {
		errMsg := "aid '" + aid + "' cannot be found"
		c.JSON(http.StatusNotFound, Error{ErrorCode: "404", ErrorMessage: errMsg})
		return
	}
	c.JSON(http.StatusOK, author.ToAPISpec())
}

// AuthorsAidPut - Add or update author information
func AuthorsAidPut(c *gin.Context) {
	contentType := c.Request.Header.Get("Content-Type")
	if contentType != "application/json" {
		c.JSON(http.StatusBadRequest, Error{ErrorCode: "400", ErrorMessage: "Expected Content-Type: 'application/json', got '" + contentType + "'"})
		return
	}

	decoder := json.NewDecoder(c.Request.Body)
	var author Author
	err := decoder.Decode(&author)
	if err != nil {
		c.JSON(http.StatusBadRequest, Error{ErrorCode: "400", ErrorMessage: err.Error()})
		return
	}

	aid := c.Param("aid")
	if author.Aid != aid {
		c.JSON(http.StatusBadRequest, Error{ErrorCode: "400", ErrorMessage: "aid in param and body do not match"})
		return
	}

	authorFhir := author.ToFHIR()
	fmt.Println(author)
	fmt.Println(authorFhir)
	jsonData, _ := json.Marshal(authorFhir)
	fhirURL, _ := ConstructURL(accessorConfig.FhirURL, "Practitioner/"+aid)
	result := SingleFHIRQuery(FHIRRequest{httpMethod: http.MethodPut, qid: aid, url: fhirURL, body: string(jsonData)})
	if result.err != nil {
		c.JSON(http.StatusInternalServerError, Error{ErrorCode: "500", ErrorMessage: result.err.Error()})
		return
	}
	c.JSON(result.statusCode, authorFhir)
}

// AuthorsGet - Mass query for author metadata in HoloStorage
func AuthorsGet(c *gin.Context) {
	fhirRequests := make(map[string]FHIRRequest)
	authorsMap := make(map[string]Author)
	aids := ParseQueryIDs(c.Query("aid"))

	for _, aid := range aids {
		fhirURL, _ := ConstructURL(accessorConfig.FhirURL, "Practitioner/"+aid)
		fhirRequests[aid] = FHIRRequest{httpMethod: http.MethodGet, qid: aid, url: fhirURL}
	}

	results := BatchFHIRQuery(fhirRequests)

	for aid, result := range results {
		var tempAuthor PractitionerFHIR
		err := json.Unmarshal(result.response, &tempAuthor)
		if err != nil {
			c.JSON(http.StatusInternalServerError, err.Error())
			return
		}
		if tempAuthor.ID != aid {
			authorsMap[aid] = Author{}
		} else {
			authorsMap[aid] = tempAuthor.ToAPISpec()
		}
	}

	c.JSON(http.StatusOK, authorsMap)
}

// HologramsGet - Mass query for hologram metadata based on hologram ids
func HologramsGet(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{})
}

// HologramsHidDelete - Delete a hologram in HoloStorage
func HologramsHidDelete(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{})
}

// HologramsHidDownloadGet - Download holograms models based on the hologram id
func HologramsHidDownloadGet(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{})
}

// HologramsHidGet - Get a single hologram metadata based on the hologram id
func HologramsHidGet(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{})
}

// HologramsPost - Upload hologram to HoloStorage
func HologramsPost(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{})
}

// PatientsGet - Mass query for patients metadata in HoloStorage
func PatientsGet(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{})
}

// PatientsPidGet - Get a single patient metadata in HoloStorage
func PatientsPidGet(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{})
}

// PatientsPidPut - Add or update basic patient information
func PatientsPidPut(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{})
}
