/*
 * HoloStorage Accessor API
 *
 * API to access holograms and metadata from HoloStorage
 *
 * API version: 1.0.0
 */

package main

import (
	"log"

	apiserver "../../internal/openapi"
)

func main() {
	router := apiserver.NewRouter()

	log.Fatal(router.Run(":8080"))
}
