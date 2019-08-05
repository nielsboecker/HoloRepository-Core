package openapi

import (
	"bytes"
	"context"
	"fmt"
	"log"
	"net/url"
	"os"

	"github.com/Azure/azure-storage-blob-go/azblob"
)

var blobContainerURL azblob.ContainerURL

func InitialiseBlobStorage(accountName, accountKey string) {
	containerName := "holograms"
	credential, err := azblob.NewSharedKeyCredential(accountName, accountKey)
	if err != nil {
		log.Fatal("Invalid blob storage credentials with error: " + err.Error())
	}

	pipeline := azblob.NewPipeline(credential, azblob.PipelineOptions{})

	URL, _ := url.Parse(fmt.Sprintf("https://%s.blob.core.windows.net/%s", accountName, containerName))

	blobContainerURL = azblob.NewContainerURL(*URL, pipeline)

	log.Printf("Creating a blob container %q\n", containerName)
	ctx := context.Background()

	_, err = blobContainerURL.Create(ctx, azblob.Metadata{}, azblob.PublicAccessNone)
	if err != nil {
		if serr, ok := err.(azblob.StorageError); ok { // This error is a Service-specific
			switch serr.ServiceCode() { // Compare serviceCode to ServiceCodeXxx constants
			case azblob.ServiceCodeContainerAlreadyExists:
				log.Printf("Blob container %q already exists.", containerName)
				return
			}
		}
		log.Fatal(err)
	}
}

func UploadHologramToBlobStorage(filename string, file *os.File) error {
	blobURL := blobContainerURL.NewBlockBlobURL(filename)
	ctx := context.Background()
	_, err := azblob.UploadFileToBlockBlob(ctx, file, blobURL, azblob.UploadToBlockBlobOptions{
		BlockSize:   4 * 1024 * 1024,
		Parallelism: 16})
	if err != nil {
		return err
	}
	return nil
}

func DownloadHologramFromBlobStorage(filename string) (bytes.Buffer, error) {
	blobURL := blobContainerURL.NewBlockBlobURL(filename)
	ctx := context.Background()
	downloadResponse, _ := blobURL.Download(ctx, 0, azblob.CountToEnd, azblob.BlobAccessConditions{}, false)
	bodyStream := downloadResponse.Body(azblob.RetryReaderOptions{MaxRetryRequests: 20})
	downloadedData := bytes.Buffer{}
	_, err := downloadedData.ReadFrom(bodyStream)
	if err != nil {
		return bytes.Buffer{}, err
	}
	return downloadedData, nil
}
