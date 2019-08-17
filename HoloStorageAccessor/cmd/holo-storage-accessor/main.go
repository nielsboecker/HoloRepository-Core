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

	apiserver "../../internal/holostorageaccessor"
)

func main() {
	config, err := apiserver.LoadConfiguration()
	if err != nil {
		log.Fatalf("Load config error: %s\n", err.Error())
	}

	err = apiserver.InitialiseBlobStorage(config.BlobStorageName, config.BlobStorageKey)
	if err != nil {
		log.Fatalf("BlobStorage init error: %s\n", err.Error())
	}

	router := apiserver.NewRouter(config)

	log.Fatal(router.Run(":3200"))
}
