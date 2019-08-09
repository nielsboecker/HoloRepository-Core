package holostorageaccessor

import (
	"testing"

	"github.com/google/go-cmp/cmp"
)

func TestPersonNameToHumanNameFHIR(t *testing.T) {
	type test struct {
		input PersonName
		want  HumanNameFHIR
	}

	tests := map[string]test{
		"full_info": {
			input: PersonName{Full: "Martin Portebello", Title: "Mr", Given: "Martin", Family: "Portebello"},
			want:  HumanNameFHIR{Text: "Martin Portebello", Family: "Portebello", Given: []string{"Martin"}, Prefix: []string{"Mr"}},
		},
		"no_info": {
			input: PersonName{},
			want:  HumanNameFHIR{},
		},
		"no_title_and_given": {
			input: PersonName{Full: "Martin Portebello", Family: "Portebello"},
			want:  HumanNameFHIR{Text: "Martin Portebello", Family: "Portebello"},
		},
		"no_full_and_family": {
			input: PersonName{Title: "Mr", Given: "Martin"},
			want:  HumanNameFHIR{Given: []string{"Martin"}, Prefix: []string{"Mr"}},
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

func TestHumanNameFHIRToPersonName(t *testing.T) {
	type test struct {
		input HumanNameFHIR
		want  PersonName
	}

	tests := map[string]test{
		"full_info": {
			input: HumanNameFHIR{Text: "Martin Portebello", Family: "Portebello", Given: []string{"Martin"}, Prefix: []string{"Mr"}},
			want:  PersonName{Full: "Martin Portebello", Title: "Mr", Given: "Martin", Family: "Portebello"},
		},
		"full_info_extra_fields": {
			input: HumanNameFHIR{Text: "Martin Portebello", Family: "Portebello", Given: []string{"Martin", "Timothy"}, Prefix: []string{"Mr", "Junior"}},
			want:  PersonName{Full: "Martin Portebello", Title: "Mr", Given: "Martin", Family: "Portebello"},
		},
		"no_info": {
			input: HumanNameFHIR{},
			want:  PersonName{},
		},
		"no_title_and_given": {
			input: HumanNameFHIR{Text: "Martin Portebello", Family: "Portebello"},
			want:  PersonName{Full: "Martin Portebello", Family: "Portebello"},
		},
		"no_full_and_family": {
			input: HumanNameFHIR{Given: []string{"Martin"}, Prefix: []string{"Mr"}},
			want:  PersonName{Title: "Mr", Given: "Martin"},
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
