/*
 * HoloStorage Accessor API
 *
 * API to access holograms and metadata from HoloStorage
 *
 * API version: 1.0.0
 */

package openapi

// PersonName - Components that make up the name of a person
type PersonName struct {
	Full   string `json:"full,omitempty"`
	Title  string `json:"title,omitempty"`
	Given  string `json:"given,omitempty"`
	Family string `json:"family,omitempty"`
}

// HumanNameFHIR - Components of the relevant FHIR HumanName resource
type HumanNameFHIR struct {
	Text   string   `json:"text,omitempty"`
	Family string   `json:"family,omitempty"`
	Given  []string `json:"given,omitempty"`
	Prefix []string `json:"prefix,omitempty"`
}

// ToFHIRSchema - Convert PersonName schema to FHIR HumanName schema
func (p PersonName) ToFHIR() HumanNameFHIR {
	var name HumanNameFHIR
	name.Text = p.Full
	name.Family = p.Family
	if p.Title != "" {
		name.Prefix = []string{p.Title}
	}
	if p.Given != "" {
		name.Given = []string{p.Given}
	}
	return name
}

// ToAPISpec - Convert FHIR HumanName schema to API Spec
func (p HumanNameFHIR) ToAPISpec() PersonName {
	var name PersonName
	name.Full = p.Text
	name.Family = p.Family
	if len(p.Prefix) > 0 {
		name.Title = p.Prefix[0]
	}
	if len(p.Given) > 0 {
		name.Given = p.Given[0]
	}

	return name
}
