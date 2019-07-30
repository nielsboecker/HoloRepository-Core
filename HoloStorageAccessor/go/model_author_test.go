package openapi

import (
	"testing"

	"github.com/google/go-cmp/cmp"
)

func TestAuthorAPISpecToPractitionerFHIR(t *testing.T) {
	type test struct {
		input Author
		want  PractitionerFHIR
	}

	tests := map[string]test{
		"all_info": {
			input: Author{Aid: "123", Name: PersonName{Full: "Bobby Cane", Title: "Mr", Given: "Bobby", Family: "Cane"}},
			want: PractitionerFHIR{
				ResourceType: "Practitioner",
				ID:           "123",
				Name: []HumanNameFHIR{
					HumanNameFHIR{
						Text:   "Bobby Cane",
						Given:  []string{"Bobby"},
						Family: "Cane",
						Prefix: []string{"Mr"}},
				}},
		},
		"partial_info": {
			input: Author{Aid: "123"},
			want:  PractitionerFHIR{ResourceType: "Practitioner", ID: "123"},
		},
		"no_info": {
			input: Author{},
			want:  PractitionerFHIR{ResourceType: "Practitioner"},
		},
	}

	for name, tc := range tests {
		t.Run(name, func(t *testing.T) {
			got := tc.input.ToFHIR()
			diff := cmp.Diff(tc.want, got)
			if diff != "" {
				t.Fatalf(diff)
			}
		})
	}
}

func TestPractitionerFHIRToAuthorAPISpec(t *testing.T) {
	type test struct {
		input PractitionerFHIR
		want  Author
	}

	tests := map[string]test{
		"all_info": {
			input: PractitionerFHIR{
				ResourceType: "Practitioner",
				ID:           "123",
				Name: []HumanNameFHIR{
					HumanNameFHIR{
						Text:   "Bobby Cane",
						Given:  []string{"Bobby"},
						Family: "Cane",
						Prefix: []string{"Mr"}},
				},
			},
			want: Author{Aid: "123", Name: PersonName{Full: "Bobby Cane", Title: "Mr", Given: "Bobby", Family: "Cane"}},
		},
		"multiple_names": {
			input: PractitionerFHIR{
				ResourceType: "Practitioner",
				ID:           "123",
				Name: []HumanNameFHIR{
					HumanNameFHIR{
						Text:   "Bobby Cane",
						Given:  []string{"Bobby"},
						Family: "Cane",
						Prefix: []string{"Mr"}},
					HumanNameFHIR{
						Text:   "Isaac Newton",
						Given:  []string{"Issac"},
						Family: "Newton",
						Prefix: []string{"Mr"}},
				},
			},
			want: Author{Aid: "123", Name: PersonName{Full: "Bobby Cane", Title: "Mr", Given: "Bobby", Family: "Cane"}},
		},
		"all_info_extra_name_fields": {
			input: PractitionerFHIR{
				ResourceType: "Practitioner",
				ID:           "123",
				Name: []HumanNameFHIR{
					HumanNameFHIR{
						Text:   "Bobby Cane",
						Given:  []string{"Bobby", "Tobias"},
						Family: "Cane",
						Prefix: []string{"Mr", "Mister"}},
				},
			},
			want: Author{Aid: "123", Name: PersonName{Full: "Bobby Cane", Title: "Mr", Given: "Bobby", Family: "Cane"}},
		},
		"partial_info": {
			input: PractitionerFHIR{ResourceType: "Practitioner", ID: "123"},
			want:  Author{Aid: "123"},
		},
		"no_info": {
			input: PractitionerFHIR{},
			want:  Author{},
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
