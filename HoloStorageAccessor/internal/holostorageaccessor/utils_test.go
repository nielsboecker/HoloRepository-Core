package holostorageaccessor

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

func TestVerifyHologramQuery(t *testing.T) {
	type test struct {
		in_hid          string
		in_pid          string
		in_creationMode string

		want_details HologramQueryDetails
		want_err     string
	}

	tests := map[string]test{
		"no_input":                             {in_hid: "", in_pid: "", in_creationMode: "", want_details: HologramQueryDetails{}, want_err: "No hids or pids were provided for this query"},
		"hid_only":                             {in_hid: "h1,h2", in_pid: "", in_creationMode: "", want_details: HologramQueryDetails{IDs: []string{"h1", "h2"}, Mode: "hologram"}},
		"pid_only":                             {in_hid: "", in_pid: "p1,p2", in_creationMode: "", want_details: HologramQueryDetails{IDs: []string{"p1", "p2"}, Mode: "patient"}},
		"both_hid_and_pid":                     {in_hid: "h1,h2", in_pid: "p1,p2", in_creationMode: "", want_details: HologramQueryDetails{}, want_err: "Use either pid or hid, not both"},
		"creation_generate_from_imaging_study": {in_hid: "", in_pid: "p1", in_creationMode: "GENERATE_FROM_IMAGING_STUDY", want_details: HologramQueryDetails{IDs: []string{"p1"}, Mode: "patient", CreationMode: "GENERATE_FROM_IMAGING_STUDY"}},
		"creation_upload_existing_model":       {in_hid: "", in_pid: "p1", in_creationMode: "UPLOAD_EXISTING_MODEL", want_details: HologramQueryDetails{IDs: []string{"p1"}, Mode: "patient", CreationMode: "UPLOAD_EXISTING_MODEL"}},
		"creation_from_depthvisor_recording":   {in_hid: "", in_pid: "p1", in_creationMode: "FROM_DEPTHVISOR_RECORDING", want_details: HologramQueryDetails{IDs: []string{"p1"}, Mode: "patient", CreationMode: "FROM_DEPTHVISOR_RECORDING"}},
		"creation_invalid":                     {in_hid: "", in_pid: "p1", in_creationMode: "invalid", want_details: HologramQueryDetails{}, want_err: "Invalid value used in creationmode. Expecting: GENERATE_FROM_IMAGING_STUDY, UPLOAD_EXISTING_MODEL, FROM_DEPTHVISOR_RECORDING"},
	}

	for name, tc := range tests {
		t.Run(name, func(t *testing.T) {
			got, err := VerifyHologramQuery(tc.in_hid, tc.in_pid, tc.in_creationMode)
			diff := cmp.Diff(tc.want_details, got)
			if diff != "" {
				t.Fatalf(diff)
			}
			if err != nil && tc.want_err != "" {
				err_diff := cmp.Diff(tc.want_err, err.Error())
				if err_diff != "" {
					t.Fatalf(err_diff)
				}
			} else if err != nil {
				t.Fatalf("Error not wanted but returned: " + err.Error())
			} else if tc.want_err != "" {
				t.Fatalf("Error wanted but not returned: " + tc.want_err)
			}
		})
	}
}
