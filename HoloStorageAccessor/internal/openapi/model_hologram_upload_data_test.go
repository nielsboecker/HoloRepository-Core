/*
 * HoloStorage Accessor API
 *
 * API to access holograms and metadata from HoloStorage
 *
 * API version: 1.0.0
 */

package openapi

import (
	"testing"
	"time"

	"github.com/google/go-cmp/cmp"
)

func TestGetHologramDataFromUpload(t *testing.T) {
	ts_creation := time.Date(2019, 1, 2, 12, 30, 45, 0, time.UTC)
	ts_imaging := time.Date(2017, 07, 15, 15, 20, 25, 0, time.UTC)

	type test struct {
		input HologramUploadData
		want  Hologram
	}

	tests := map[string]test{
		"no_info": {
			input: HologramUploadData{},
			want:  Hologram{},
		},
		"all_info": {
			input: HologramUploadData{
				Title:               "Hologram Title",
				Description:         "Hologram Description",
				ContentType:         "model/gltf-binary",
				FileSizeInKb:        1000,
				BodySite:            "Hips",
				DateOfImaging:       &ts_imaging,
				CreationDate:        &ts_creation,
				CreationMode:        "GENERATE_FROM_IMAGING_STUDY",
				CreationDescription: "From bone segmentation pipeline with HU threshold of 750",
				Author:              Author{Aid: "author-456", Name: &PersonName{Full: "Timothy David", Given: "Timothy", Family: "David", Title: "Dr"}},
				Patient:             Patient{Pid: "patient-123", BirthDate: "2019-01-01", Gender: "female", Name: &PersonName{Full: "Bobby Cane", Title: "Mr", Given: "Bobby", Family: "Cane"}},
			},
			want: Hologram{
				Title:               "Hologram Title",
				Description:         "Hologram Description",
				ContentType:         "model/gltf-binary",
				FileSizeInKb:        1000,
				BodySite:            "Hips",
				DateOfImaging:       &ts_imaging,
				CreationDate:        &ts_creation,
				CreationMode:        "GENERATE_FROM_IMAGING_STUDY",
				CreationDescription: "From bone segmentation pipeline with HU threshold of 750",
				Aid:                 "author-456",
				Pid:                 "patient-123",
			},
		},
	}

	for name, tc := range tests {
		t.Run(name, func(t *testing.T) {
			got := tc.input.GetHologramData()
			diff := cmp.Diff(tc.want, got)
			if diff != "" {
				t.Fatalf(diff)
			}
		})
	}
}

func TestGetHologramDocRefDataFromHologramUpload(t *testing.T) {
	ts_creation := time.Date(2019, 1, 2, 12, 30, 45, 0, time.UTC)
	ts_imaging := time.Date(2017, 07, 15, 15, 20, 25, 0, time.UTC)

	type test struct {
		input HologramUploadData
		want  HologramDocumentReferenceFHIR
	}

	tests := map[string]test{
		"no_info": {
			input: HologramUploadData{},
			want: HologramDocumentReferenceFHIR{
				ResourceType: "DocumentReference",
				Status:       "current",
			},
		},
		"all_info": {
			input: HologramUploadData{
				Title:               "Hologram Title",
				Description:         "Hologram Description",
				ContentType:         "model/gltf-binary",
				FileSizeInKb:        1000,
				BodySite:            "Hips",
				DateOfImaging:       &ts_imaging,
				CreationDate:        &ts_creation,
				CreationMode:        "GENERATE_FROM_IMAGING_STUDY",
				CreationDescription: "From bone segmentation pipeline with HU threshold of 750",
				Author:              Author{Aid: "author-456", Name: &PersonName{Full: "Timothy David", Given: "Timothy", Family: "David", Title: "Dr"}},
				Patient:             Patient{Pid: "patient-123", BirthDate: "2019-01-01", Gender: "female", Name: &PersonName{Full: "Bobby Cane", Title: "Mr", Given: "Bobby", Family: "Cane"}},
			},
			want: HologramDocumentReferenceFHIR{
				ResourceType: "DocumentReference",
				Status:       "current",
				Date:         &ts_creation,
				Type:         CodeableConceptFHIR{Text: "GENERATE_FROM_IMAGING_STUDY"},
				HologramMeta: `{"description":"Hologram Description","creationDescription":"From bone segmentation pipeline with HU threshold of 750","bodySite":"Hips","dateOfImaging":"2017-07-15T15:20:25Z"}`,
				Content: []ContentFHIR{ContentFHIR{Attachment: AttachmentFHIR{
					ContentType: "model/gltf-binary",
					Size:        1024000,
					Title:       "Hologram Title",
				}}},
				Subject: ReferenceFHIR{Reference: "Patient/patient-123"},
				Author:  []ReferenceFHIR{ReferenceFHIR{Reference: "Practitioner/author-456"}},
			},
		},
	}

	for name, tc := range tests {
		t.Run(name, func(t *testing.T) {
			got := tc.input.GetHologramDataInDocRefFHIR()
			diff := cmp.Diff(tc.want, got)
			if diff != "" {
				t.Fatalf(diff)
			}
		})
	}
}
