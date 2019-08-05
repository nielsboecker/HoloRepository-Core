/*
 * HoloStorage Accessor API
 *
 * API to access holograms and metadata from HoloStorage
 *
 * API version: 1.0.0
 */

package openapi

import (
	"log"
	"net/http"

	"github.com/gin-gonic/gin"
)

// Route is the information for every URI.
type Route struct {
	// Name is the name of this Route.
	Name string
	// Method is the string for the HTTP method. ex) GET, POST etc..
	Method string
	// Pattern is the pattern of the URI.
	Pattern string
	// HandlerFunc is the handler function of this route.
	HandlerFunc gin.HandlerFunc
}

// Routes is the list of the generated Route.
type Routes []Route

type AccessorConfig struct {
	FhirURL         string
	BlobStorageName string
	BlobStorageKey  string
}

var basePathComponent = "/api/1.0.0/"
var uiPath = basePathComponent + "ui/"
var accessorConfig AccessorConfig

// NewRouter returns a new router.
func NewRouter() *gin.Engine {
	err := LoadConfiguration(&accessorConfig)
	if err != nil {
		log.Fatalln(err)
	}

	log.Printf("FHIR Backend URL: %q", accessorConfig.FhirURL)
	log.Printf("Blob Store: %q", accessorConfig.BlobStorageName)

	router := gin.Default()

	router.Static(uiPath, "./third_party/swaggerui")

	for _, route := range routes {
		switch route.Method {
		case http.MethodGet:
			router.GET(route.Pattern, route.HandlerFunc)
		case http.MethodPost:
			router.POST(route.Pattern, route.HandlerFunc)
		case http.MethodPut:
			router.PUT(route.Pattern, route.HandlerFunc)
		case http.MethodDelete:
			router.DELETE(route.Pattern, route.HandlerFunc)
		}
	}

	return router
}

// Index is the index handler.
func Index(c *gin.Context) {
	welcome := "HoloStorage Accessor is running! View the different API endpoints at " + uiPath
	c.String(http.StatusOK, welcome)
}

var routes = Routes{
	{
		"Index",
		http.MethodGet,
		basePathComponent,
		Index,
	},

	{
		"AuthorsAidGet",
		http.MethodGet,
		basePathComponent + "authors/:aid",
		AuthorsAidGet,
	},

	{
		"AuthorsAidPut",
		http.MethodPut,
		basePathComponent + "authors/:aid",
		AuthorsAidPut,
	},

	{
		"AuthorsGet",
		http.MethodGet,
		basePathComponent + "authors",
		AuthorsGet,
	},

	{
		"HologramsGet",
		http.MethodGet,
		basePathComponent + "holograms",
		HologramsGet,
	},

	{
		"HologramsHidDelete",
		http.MethodDelete,
		basePathComponent + "holograms/:hid",
		HologramsHidDelete,
	},

	{
		"HologramsHidDownloadGet",
		http.MethodGet,
		basePathComponent + "holograms/:hid/download",
		HologramsHidDownloadGet,
	},

	{
		"HologramsHidGet",
		http.MethodGet,
		basePathComponent + "holograms/:hid",
		HologramsHidGet,
	},

	{
		"HologramsPost",
		http.MethodPost,
		basePathComponent + "holograms",
		HologramsPost,
	},

	{
		"PatientsGet",
		http.MethodGet,
		basePathComponent + "patients",
		PatientsGet,
	},

	{
		"PatientsPidGet",
		http.MethodGet,
		basePathComponent + "patients/:pid",
		PatientsPidGet,
	},

	{
		"PatientsPidPut",
		http.MethodPut,
		basePathComponent + "patients/:pid",
		PatientsPidPut,
	},
}
