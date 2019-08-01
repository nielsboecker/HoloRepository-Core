package openapi

import (
	"testing"
	"time"

	"bou.ke/monkey"
	"github.com/google/go-cmp/cmp"
)

func TestHologramToHologramDocumentReferenceFHIR(t *testing.T) {
	monkey.Patch(time.Now, func() time.Time {
		return time.Date(2019, 10, 15, 20, 35, 55, 0, time.UTC)
	})

	type test struct {
		input Hologram
		url   string
		want  HologramDocumentReferenceFHIR
	}

	tests := map[string]test{
		"empty": {
			input: Hologram{},
			url:   "",
			want: HologramDocumentReferenceFHIR{
				ResourceType: "DocumentReference",
				Status:       "current",
			},
		},
		"with_data": {
			input: Hologram{
				Hid:                 "123",
				Title:               "test-title",
				Description:         "test-description",
				ContentType:         "application/test",
				FileSizeInKb:        1000,
				CreationDate:        time.Date(2019, 1, 2, 12, 30, 45, 0, time.UTC),
				CreationMode:        "GENERATE_FROM_IMAGING_STUDY",
				CreationDescription: "test-pipe",
				DateOfImaging:       time.Date(2017, 07, 15, 15, 20, 25, 0, time.UTC),
				BodySite:            "hips",
			},
			url: "www.storage.com/download/12345",
			want: HologramDocumentReferenceFHIR{
				ResourceType: "DocumentReference",
				Status:       "current",
				Date:         time.Date(2019, 1, 2, 12, 30, 45, 0, time.UTC),
				ID:           "123",
				Type:         CodeableConceptFHIR{Text: "GENERATE_FROM_IMAGING_STUDY"},
				HologramMeta: `{"description":"test-description","creationDescription":"test-pipe","bodySite":"hips","dateOfImaging":"2017-07-15T15:20:25Z"}`,
				Content: []ContentFHIR{ContentFHIR{Attachment: AttachmentFHIR{
					ContentType: "application/test",
					Size:        1024000,
					Title:       "test-title",
					URL:         "www.storage.com/download/12345",
				}}},
			},
		},
	}

	for name, tc := range tests {
		t.Run(name, func(t *testing.T) {
			got := tc.input.ToFHIR()
			_ = got.UpdateAttachmentURL(tc.url)
			diff := cmp.Diff(tc.want, got)
			if diff != "" {
				t.Fatalf(diff)
			}
		})
	}
}

func TestHologramDocumentReferenceFHIRToHologram(t *testing.T) {
	monkey.Patch(time.Now, func() time.Time {
		return time.Date(2019, 10, 15, 20, 35, 55, 0, time.UTC)
	})

	type test struct {
		input HologramDocumentReferenceFHIR
		want  Hologram
	}

	tests := map[string]test{
		"empty": {
			want: Hologram{},
			input: HologramDocumentReferenceFHIR{
				ResourceType: "DocumentReference",
				Status:       "current",
			},
		},
		"with_data:": {
			input: HologramDocumentReferenceFHIR{
				ResourceType: "DocumentReference",
				Status:       "current",
				Date:         time.Date(2019, 1, 2, 12, 30, 45, 0, time.UTC),
				ID:           "123",
				Type:         CodeableConceptFHIR{Text: "GENERATE_FROM_IMAGING_STUDY"},
				HologramMeta: `{"description":"test-description","creationDescription":"test-pipe","bodySite":"hips","dateOfImaging":"2017-07-15T15:20:25Z"}`,
				Content: []ContentFHIR{ContentFHIR{Attachment: AttachmentFHIR{
					ContentType: "application/test",
					Size:        1024000,
					Title:       "test-title",
					URL:         "www.storage.com/download/12345",
				}}},
			},
			want: Hologram{
				Hid:                 "123",
				Title:               "test-title",
				Description:         "test-description",
				ContentType:         "application/test",
				FileSizeInKb:        1000,
				CreationDate:        time.Date(2019, 1, 2, 12, 30, 45, 0, time.UTC),
				CreationMode:        "GENERATE_FROM_IMAGING_STUDY",
				CreationDescription: "test-pipe",
				DateOfImaging:       time.Date(2017, 07, 15, 15, 20, 25, 0, time.UTC),
				BodySite:            "hips",
			},
		},
	}

	for name, tc := range tests {
		t.Run(name, func(t *testing.T) {
			got := tc.input.ToAPISpec()
			diff := cmp.Diff(tc.want, got)
			if diff != "" {
				t.Fatalf(diff)
			}
		})
	}
}
