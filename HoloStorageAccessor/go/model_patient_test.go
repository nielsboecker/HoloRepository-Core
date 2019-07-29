package openapi

import (
	"testing"

	"github.com/google/go-cmp/cmp"
)

func TestPatientAPISpecToPatientFHIR(t *testing.T) {
	type test struct {
		input Patient
		want  PatientFHIR
	}

	tests := map[string]test{
		"all_info": {
			input: Patient{Pid: "123", BirthDate: "2019-01-01", Gender: "female", Name: PersonName{Full: "Bobby Cane", Title: "Mr", Given: "Bobby", Family: "Cane"}},
			want:  PatientFHIR{ResourceType: "Patient", ID: "123", Gender: "female", BirthDate: "2019-01-01", Name: HumanNameFHIR{Text: "Bobby Cane", Given: []string{"Bobby"}, Family: "Cane", Prefix: []string{"Mr"}}},
		},
		"partial_info": {
			input: Patient{Pid: "123", Gender: "female"},
			want:  PatientFHIR{ResourceType: "Patient", ID: "123", Gender: "female"},
		},
		"no_info": {
			input: Patient{},
			want:  PatientFHIR{ResourceType: "Patient"},
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

func TestPatientFHIRToPatientAPISpec(t *testing.T) {
	type test struct {
		input PatientFHIR
		want  Patient
	}

	tests := map[string]test{
		"all_info": {
			input: PatientFHIR{ResourceType: "Patient", ID: "123", Gender: "female", BirthDate: "2019-01-01", Name: HumanNameFHIR{Text: "Bobby Cane", Given: []string{"Bobby"}, Family: "Cane", Prefix: []string{"Mr"}}},
			want:  Patient{Pid: "123", BirthDate: "2019-01-01", Gender: "female", Name: PersonName{Full: "Bobby Cane", Title: "Mr", Given: "Bobby", Family: "Cane"}},
		},
		"all_info_extra_name_fields": {
			input: PatientFHIR{ResourceType: "Patient", ID: "123", Gender: "female", BirthDate: "2019-01-01", Name: HumanNameFHIR{Text: "Bobby Cane", Given: []string{"Bobby", "Tobias"}, Family: "Cane", Prefix: []string{"Mr", "Mister"}}},
			want:  Patient{Pid: "123", BirthDate: "2019-01-01", Gender: "female", Name: PersonName{Full: "Bobby Cane", Title: "Mr", Given: "Bobby", Family: "Cane"}},
		},
		"partial_info": {
			input: PatientFHIR{ResourceType: "Patient", ID: "123", Gender: "female"},
			want:  Patient{Pid: "123", Gender: "female"},
		},
		"no_info": {
			input: PatientFHIR{},
			want:  Patient{},
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
