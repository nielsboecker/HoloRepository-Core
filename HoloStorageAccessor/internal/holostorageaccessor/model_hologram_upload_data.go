/*
 * HoloStorage Accessor API
 *
 * API to access holograms and metadata from HoloStorage
 *
 * API version: 1.0.0
 */

package holostorageaccessor

import (
	"os"
	"time"
)

// HologramUploadData - Data structure to upload holograms to HoloStorage
type HologramUploadData struct {
	Title               string     `json:"title,omitempty"`
	Description         string     `json:"description,omitempty"`
	ContentType         string     `json:"contentType,omitempty"`
	FileSizeInKb        uint32     `json:"fileSizeInKb,omitempty"`
	BodySite            string     `json:"bodySite,omitempty"`
	DateOfImaging       *time.Time `json:"dateOfImaging,omitempty"`
	CreationDate        *time.Time `json:"creationDate,omitempty"`
	CreationMode        string     `json:"creationMode,omitempty"`
	CreationDescription string     `json:"creationDescription,omitempty"`
	HologramFile        *os.File   `json:"hologramFile,omitempty"`
	Author              Author     `json:"author,omitempty"`
	Patient             Patient    `json:"patient,omitempty"`
}

func (h HologramUploadData) GetHologramData() Hologram {
	data := Hologram{
		Aid:                 h.Author.Aid,
		BodySite:            h.BodySite,
		ContentType:         h.ContentType,
		CreationDate:        h.CreationDate,
		CreationDescription: h.CreationDescription,
		CreationMode:        h.CreationMode,
		DateOfImaging:       h.DateOfImaging,
		Description:         h.Description,
		FileSizeInKb:        h.FileSizeInKb,
		Pid:                 h.Patient.Pid,
		Title:               h.Title,
	}
	return data
}

func (h HologramUploadData) GetHologramDataInDocRefFHIR() HologramDocumentReferenceFHIR {
	hologramData := h.GetHologramData()
	data := hologramData.ToFHIR()

	return data
}
