package holostorageaccessor

import (
	"net/url"
	"os"
	"testing"
	"time"

	"github.com/google/go-cmp/cmp"
)

func returnTime(timeString string) *time.Time {
	time, _ := time.Parse(time.RFC3339, timeString)
	return &time
}

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

func TestParseHologramUploadPostInput(t *testing.T) {

	type test struct {
		input    map[string]url.Values
		want     HologramPostInput
		want_err string
	}

	inputs := make(map[string]url.Values)

	inputs["empty"] = url.Values{}
	inputs["full_data"] = url.Values{}
	inputs["full_data"].Set("title", "test title")
	inputs["full_data"].Set("description", "test desc")
	inputs["full_data"].Set("contentType", "test/type")
	inputs["full_data"].Set("fileSizeInKb", "5000")
	inputs["full_data"].Set("bodySite", "test bodysite")
	inputs["full_data"].Set("dateOfImaging", "2017-11-11T11:11:11Z")
	inputs["full_data"].Set("creationDate", "2017-12-12T12:12:12Z")
	inputs["full_data"].Set("creationMode", "GENERATE_FROM_IMAGING_STUDY")
	inputs["full_data"].Set("creationDescription", "test creation desc")
	inputs["full_data"].Set("patient", `{"pid":"p2000","name":{"full":"Marvin Portebello","title":"Mr","given":"Marvin","family":"Portebello"},"gender":"male","birthDate":"2019-07-16"}`)
	inputs["full_data"].Set("author", `{"aid":"a2000","name":{"full":"Tom Sawyer","title":"Mr","given":"Tom","family":"Sawyer"}}`)
	inputs["bad_creationDate"] = url.Values{}
	inputs["bad_creationDate"].Set("creationDate", "2017-12-12T1:1:1Z")
	inputs["bad_dateOfImaging"] = url.Values{}
	inputs["bad_dateOfImaging"].Set("dateOfImaging", "2017-12-12T1:1:1Z")
	inputs["bad_filesize"] = url.Values{}
	inputs["bad_filesize"].Set("fileSizeInKb", "invalid-filesize")
	inputs["no_pid"] = url.Values{}
	inputs["no_pid"].Set("patient", `{"name":{"full":"Marvin Portebello","title":"Mr","given":"Marvin","family":"Portebello"},"gender":"male","birthDate":"2019-07-16"}`)
	inputs["bad_patient_data"] = url.Values{}
	inputs["bad_patient_data"].Set("patient", `invalid-json-content`)
	inputs["no_aid"] = url.Values{}
	inputs["no_aid"].Set("author", `{"aid":"","name":{"full":"Tom Sawyer","title":"Mr","given":"Tom","family":"Sawyer"}}`)
	inputs["bad_author_data"] = url.Values{}
	inputs["bad_author_data"].Set("author", `invalid-json-content`)

	tests := map[string]test{
		"empty":             {input: inputs, want: HologramPostInput{}},
		"bad_creationDate":  {input: inputs, want: HologramPostInput{}, want_err: "Key creationDate='2017-12-12T1:1:1Z' does not conform to RFC3339 standards"},
		"bad_dateOfImaging": {input: inputs, want: HologramPostInput{}, want_err: "Key dateOfImaging='2017-12-12T1:1:1Z' does not conform to RFC3339 standards"},
		"bad_filesize":      {input: inputs, want: HologramPostInput{}, want_err: "Key fileSizeInKb='invalid-filesize' is not a valid filesize value"},
		"no_pid":            {input: inputs, want: HologramPostInput{}, want_err: "Patient ID is required"},
		"no_aid":            {input: inputs, want: HologramPostInput{}, want_err: "Author ID is required"},
		"bad_patient_data":  {input: inputs, want: HologramPostInput{}, want_err: "Unable to parse patient data: invalid character 'i' looking for beginning of value"},
		"bad_author_data":   {input: inputs, want: HologramPostInput{}, want_err: "Unable to parse author data: invalid character 'i' looking for beginning of value"},
		"full_data": {input: inputs, want: HologramPostInput{
			Author: Author{
				Aid: "a2000",
				Name: &PersonName{
					Family: "Sawyer",
					Given:  "Tom",
					Full:   "Tom Sawyer",
					Title:  "Mr",
				},
			},
			Patient: Patient{
				Pid: "p2000", Gender: "male",
				BirthDate: "2019-07-16",
				Name: &PersonName{
					Family: "Portebello",
					Given:  "Marvin",
					Title:  "Mr",
					Full:   "Marvin Portebello",
				},
			},
			Hologram: Hologram{
				Aid:                 "a2000",
				Pid:                 "p2000",
				BodySite:            "test bodysite",
				ContentType:         "test/type",
				DateOfImaging:       returnTime("2017-11-11T11:11:11Z"),
				CreationDate:        returnTime("2017-12-12T12:12:12Z"),
				CreationMode:        "GENERATE_FROM_IMAGING_STUDY",
				CreationDescription: "test creation desc",
				Description:         "test desc",
				FileSizeInKb:        uint32(5000),
				Title:               "test title",
			},
		}},
	}

	for name, tc := range tests {
		t.Run(name, func(t *testing.T) {
			got, err := ParseHologramUploadPostInput(tc.input[name])
			diff := cmp.Diff(tc.want, got)
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

func TestLoadConfiguration(t *testing.T) {
	type test struct {
		confFields map[string]string
		want       AccessorConfig
		want_err   string
	}

	tests := map[string]test{
		"no_config": test{
			want:     AccessorConfig{},
			want_err: "Environment config field 'AZURE_STORAGE_ACCOUNT' is not set",
		},
		"bad_url": test{
			want: AccessorConfig{},
			confFields: map[string]string{
				"AZURE_STORAGE_ACCOUNT":    "account_name",
				"AZURE_STORAGE_ACCESS_KEY": "access_key",
				"ACCESSOR_FHIR_URL":        "bad-url.com",
				"ENABLE_CORS":              "false",
			},
			want_err: "ACCESSOR_FHIR_URL error: parse bad-url.com: invalid URI for request",
		},
		"bad_spaces_in_url": test{
			want: AccessorConfig{},
			confFields: map[string]string{
				"AZURE_STORAGE_ACCOUNT":    "account_name",
				"AZURE_STORAGE_ACCESS_KEY": "access_key",
				"ACCESSOR_FHIR_URL":        "http://  bad-url.com",
				"ENABLE_CORS":              "false",
			},
			want_err: `ACCESSOR_FHIR_URL error: parse http://  bad-url.com: invalid character " " in host name`,
		},
		"all_config": test{
			confFields: map[string]string{
				"AZURE_STORAGE_ACCOUNT":    "account_name",
				"AZURE_STORAGE_ACCESS_KEY": "access_key",
				"ACCESSOR_FHIR_URL":        "http://www.test.com",
				"ENABLE_CORS":              "true",
			},
			want: AccessorConfig{
				BlobStorageKey:  "access_key",
				BlobStorageName: "account_name",
				FhirURL:         "http://www.test.com",
				EnableCORS:      true,
			},
		},
		"bad_enable_cors": test{
			confFields: map[string]string{
				"AZURE_STORAGE_ACCOUNT":    "account_name",
				"AZURE_STORAGE_ACCESS_KEY": "access_key",
				"ACCESSOR_FHIR_URL":        "http://www.test.com",
				"ENABLE_CORS":              "invalid-value",
			},
			want_err: `ENABLE_CORS error: strconv.ParseBool: parsing "invalid-value": invalid syntax`,
		},
		"all_config_with_spaces": test{
			confFields: map[string]string{
				"AZURE_STORAGE_ACCOUNT":    "  account_name ",
				"AZURE_STORAGE_ACCESS_KEY": "  access_key  ",
				"ACCESSOR_FHIR_URL":        "  http://www.test.com  ",
				"ENABLE_CORS":              "  true  ",
			},
			want: AccessorConfig{
				BlobStorageKey:  "access_key",
				BlobStorageName: "account_name",
				FhirURL:         "http://www.test.com",
				EnableCORS:      true,
			},
		},
	}

	for name, tc := range tests {
		confFields := []string{
			"AZURE_STORAGE_ACCOUNT",
			"AZURE_STORAGE_ACCESS_KEY",
			"ACCESSOR_FHIR_URL",
			"ENABLE_CORS",
		}
		for _, config := range confFields {
			os.Setenv(config, "")
		}
		for key, value := range tc.confFields {
			os.Setenv(key, value)
		}
		t.Run(name, func(t *testing.T) {
			var config AccessorConfig
			err := LoadConfiguration(&config)
			diff := cmp.Diff(tc.want, config)
			if err != nil && tc.want_err != "" {
				err_diff := cmp.Diff(tc.want_err, err.Error())
				if err_diff != "" {
					t.Fatalf(err_diff)
				}
			} else if err != nil {
				t.Fatalf("Error not wanted but returned: " + err.Error())
			} else if tc.want_err != "" {
				t.Fatalf("Error wanted but not returned: " + tc.want_err)
			} else {
				if diff != "" {
					t.Fatalf(diff)
				}
			}

		})
	}
}
