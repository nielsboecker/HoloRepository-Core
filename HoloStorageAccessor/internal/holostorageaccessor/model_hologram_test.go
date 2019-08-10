package holostorageaccessor

import (
	"testing"
	"time"

	"github.com/google/go-cmp/cmp"
)

func TestHologramToHologramDocumentReferenceFHIR(t *testing.T) {
	ts_creation := time.Date(2019, 1, 2, 12, 30, 45, 0, time.UTC)
	ts_imaging := time.Date(2017, 07, 15, 15, 20, 25, 0, time.UTC)

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
				Aid:                 "a123",
				Pid:                 "p123",
				Title:               "test-title",
				Description:         "test-description",
				ContentType:         "application/test",
				FileSizeInKb:        1000,
				CreationDate:        &ts_creation,
				CreationMode:        "GENERATE_FROM_IMAGING_STUDY",
				CreationDescription: "test-pipe",
				DateOfImaging:       &ts_imaging,
				BodySite:            "hips",
			},
			url: "www.storage.com/download/12345",
			want: HologramDocumentReferenceFHIR{
				ResourceType: "DocumentReference",
				Status:       "current",
				Date:         &ts_creation,
				ID:           "123",
				Type:         CodeableConceptFHIR{Text: "GENERATE_FROM_IMAGING_STUDY"},
				HologramMeta: `{"description":"test-description","creationDescription":"test-pipe","bodySite":"hips","dateOfImaging":"2017-07-15T15:20:25Z"}`,
				Content: []ContentFHIR{ContentFHIR{Attachment: AttachmentFHIR{
					ContentType: "application/test",
					Size:        1024000,
					Title:       "test-title",
					URL:         "www.storage.com/download/12345",
				}}},
				Subject: ReferenceFHIR{Reference: "Patient/p123"},
				Author:  []ReferenceFHIR{ReferenceFHIR{Reference: "Practitioner/a123"}},
			},
		},
		"with_some_missing_attachment_data": {
			input: Hologram{
				Hid:                 "123",
				Aid:                 "a123",
				Pid:                 "p123",
				Title:               "",
				Description:         "",
				ContentType:         "application/test",
				FileSizeInKb:        1000,
				CreationDate:        &ts_creation,
				CreationMode:        "GENERATE_FROM_IMAGING_STUDY",
				CreationDescription: "test-pipe",
				DateOfImaging:       &ts_imaging,
				BodySite:            "hips",
			},
			url: "www.storage.com/download/12345",
			want: HologramDocumentReferenceFHIR{
				ResourceType: "DocumentReference",
				Status:       "current",
				Date:         &ts_creation,
				ID:           "123",
				Type:         CodeableConceptFHIR{Text: "GENERATE_FROM_IMAGING_STUDY"},
				HologramMeta: `{"creationDescription":"test-pipe","bodySite":"hips","dateOfImaging":"2017-07-15T15:20:25Z"}`,
				Content: []ContentFHIR{ContentFHIR{Attachment: AttachmentFHIR{
					ContentType: "application/test",
					Size:        1024000,
					URL:         "www.storage.com/download/12345",
				}}},
				Subject: ReferenceFHIR{Reference: "Patient/p123"},
				Author:  []ReferenceFHIR{ReferenceFHIR{Reference: "Practitioner/a123"}},
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
	ts_creation := time.Date(2019, 1, 2, 12, 30, 45, 0, time.UTC)
	ts_imaging := time.Date(2017, 07, 15, 15, 20, 25, 0, time.UTC)

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
				Date:         &ts_creation,
				ID:           "123",
				Type:         CodeableConceptFHIR{Text: "GENERATE_FROM_IMAGING_STUDY"},
				HologramMeta: `{"description":"test-description","creationDescription":"test-pipe","bodySite":"hips","dateOfImaging":"2017-07-15T15:20:25Z"}`,
				Content: []ContentFHIR{ContentFHIR{Attachment: AttachmentFHIR{
					ContentType: "application/test",
					Size:        1024000,
					Title:       "test-title",
					URL:         "www.storage.com/download/12345",
				}}},
				Subject: ReferenceFHIR{Reference: "Patient/p123"},
				Author:  []ReferenceFHIR{ReferenceFHIR{Reference: "Practitioner/a123"}},
			},
			want: Hologram{
				Hid:                 "123",
				Pid:                 "p123",
				Aid:                 "a123",
				Title:               "test-title",
				Description:         "test-description",
				ContentType:         "application/test",
				FileSizeInKb:        1000,
				CreationDate:        &ts_creation,
				CreationMode:        "GENERATE_FROM_IMAGING_STUDY",
				CreationDescription: "test-pipe",
				DateOfImaging:       &ts_imaging,
				BodySite:            "hips",
			},
		},
		"with_data_missing_prefix:": {
			input: HologramDocumentReferenceFHIR{
				ResourceType: "DocumentReference",
				Status:       "current",
				Date:         &ts_creation,
				ID:           "123",
				Type:         CodeableConceptFHIR{Text: "GENERATE_FROM_IMAGING_STUDY"},
				HologramMeta: `{"description":"test-description","creationDescription":"test-pipe","bodySite":"hips","dateOfImaging":"2017-07-15T15:20:25Z"}`,
				Content: []ContentFHIR{ContentFHIR{Attachment: AttachmentFHIR{
					ContentType: "application/test",
					Size:        1024000,
					Title:       "test-title",
					URL:         "www.storage.com/download/12345",
				}}},
				Subject: ReferenceFHIR{Reference: "p123"},
				Author:  []ReferenceFHIR{ReferenceFHIR{Reference: "a123"}},
			},
			want: Hologram{
				Hid:                 "123",
				Pid:                 "p123",
				Aid:                 "a123",
				Title:               "test-title",
				Description:         "test-description",
				ContentType:         "application/test",
				FileSizeInKb:        1000,
				CreationDate:        &ts_creation,
				CreationMode:        "GENERATE_FROM_IMAGING_STUDY",
				CreationDescription: "test-pipe",
				DateOfImaging:       &ts_imaging,
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
