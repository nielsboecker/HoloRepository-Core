package openapi

import (
	"bytes"
	"context"
	"fmt"
	"io"
	"log"
	"net/url"

	"github.com/Azure/azure-storage-blob-go/azblob"
)

var blobContainerURL azblob.ContainerURL

func InitialiseBlobStorage(accountName, accountKey string) error {
	containerName := "holograms"
	credential, err := azblob.NewSharedKeyCredential(accountName, accountKey)
	if err != nil {
		return fmt.Errorf("Invalid blob storage credentials with error: " + err.Error())
	}

	pipeline := azblob.NewPipeline(credential, azblob.PipelineOptions{})

	URL, _ := url.Parse(fmt.Sprintf("https://%s.blob.core.windows.net/%s", accountName, containerName))

	blobContainerURL = azblob.NewContainerURL(*URL, pipeline)

	log.Printf("Creating a blob container %q\n", containerName)
	ctx := context.Background()

	_, err = blobContainerURL.Create(ctx, azblob.Metadata{}, azblob.PublicAccessNone)
	if err != nil {
		if serr, ok := err.(azblob.StorageError); ok {
			switch serr.ServiceCode() {
			case azblob.ServiceCodeContainerAlreadyExists:
				log.Printf("Blob container %q already exists.", containerName)
				return nil
			}
		}
		return err
	}
	return nil
}

func UploadHologramToBlobStorage(filename string, filedata io.Reader) error {
	blobURL := blobContainerURL.NewBlockBlobURL(filename)
	ctx := context.Background()
	bufferSize := 2 * 1024 * 1024 // Configure the size of the rotating buffers that are used when uploading
	maxBuffers := 20              // Configure the number of rotating buffers that are used when uploading
	_, err := azblob.UploadStreamToBlockBlob(ctx, filedata, blobURL,
		azblob.UploadStreamToBlockBlobOptions{BufferSize: bufferSize, MaxBuffers: maxBuffers})
	if err != nil {
		return err
	}
	return nil
}

func DownloadHologramFromBlobStorage(filename string) (bytes.Buffer, error) {
	blobURL := blobContainerURL.NewBlockBlobURL(filename)
	ctx := context.Background()
	downloadResponse, err := blobURL.Download(ctx, 0, azblob.CountToEnd, azblob.BlobAccessConditions{}, false)
	if err != nil {
		return bytes.Buffer{}, err
	}
	bodyStream := downloadResponse.Body(azblob.RetryReaderOptions{MaxRetryRequests: 20})
	downloadedData := bytes.Buffer{}
	_, err = downloadedData.ReadFrom(bodyStream)
	if err != nil {
		return bytes.Buffer{}, err
	}
	return downloadedData, nil
}

func DeleteHologramFromBlobStorage(filename string) error {
	// TODO
	return nil
}
