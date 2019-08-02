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
		"multiple_queries":   {input: "100,200,300", want: []string{"100", "200", "300"}},
		"trialing_comma":     {input: "100,200,", want: []string{"100", "200"}},
		"single_query":       {input: "100", want: []string{"100"}},
		"no_query":           {input: "", want: []string{""}},
		"duplicated_queries": {input: "100,100", want: []string{"100"}},
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

func TestURLPathConstruction(t *testing.T) {
	type test struct {
		baseurl string
		path    string
		want    string
	}

	tests := map[string]test{
		"no_path_components":                       {baseurl: "http://test.com", path: "", want: "http://test.com"},
		"with_path":                                {baseurl: "http://test.com", path: "demo/path", want: "http://test.com/demo/path"},
		"baseurl_trailing_slash":                   {baseurl: "http://test.com/", path: "demo/path", want: "http://test.com/demo/path"},
		"path_leading_slash":                       {baseurl: "http://test.com", path: "/demo/path", want: "http://test.com/demo/path"},
		"basepath_trailing_and_path_leading_slash": {baseurl: "http://test.com/", path: "/demo/path", want: "http://test.com/demo/path"},
		"path_trailing_slash":                      {baseurl: "http://test.com", path: "demo/path/", want: "http://test.com/demo/path"},
	}

	for name, tc := range tests {
		t.Run(name, func(t *testing.T) {
			got, _ := ConstructURL(tc.baseurl, tc.path)
			diff := cmp.Diff(tc.want, got)
			if diff != "" {
				t.Fatalf(diff)
			}
		})
	}
}
