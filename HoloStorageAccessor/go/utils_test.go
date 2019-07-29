package openapi

import (
	"testing"

	"github.com/google/go-cmp/cmp"
)

func TestGetAllQueryIDs(t *testing.T) {
	type test struct {
		input string
		want  []string
	}

	tests := map[string]test{
		"Multiple queries": {input: "100,200,300", want: []string{"100", "200", "300"}},
		"Trailing comma":   {input: "100,200,", want: []string{"100", "200"}},
		"Single query":     {input: "100", want: []string{"100"}},
		"No query":         {input: "", want: []string{""}},
	}

	for name, tc := range tests {
		t.Run(name, func(t *testing.T) {
			got := ParseQueryIDs(tc.input)
			diff := cmp.Diff(tc.want, got)
			if diff != "" {
				t.Fatalf(diff)
			}
		})
	}
}
