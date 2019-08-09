/*
 * HoloStorage Accessor API
 *
 * API to access holograms and metadata from HoloStorage
 *
 * API version: 1.0.0
 */

package holostorageaccessor

// Author - Who authored the Hologram
type Author struct {
	Aid  string      `json:"aid,omitempty"`
	Name *PersonName `json:"name,omitempty"`
}

// PractitionerFHIR - Components of the relevant Practitioner FHIR resource
type PractitionerFHIR struct {
	ResourceType string          `json:"resourceType"`
	ID           string          `json:"id"`
	Name         []HumanNameFHIR `json:"name,omitempty"`
}

// ToFHIR - Convert PractitionerBasic schema to FHIR Practitioner schema
func (r Author) ToFHIR() PractitionerFHIR {
	fhirData := PractitionerFHIR{ResourceType: "Practitioner"}
	fhirData.ID = r.Aid

	if r.Name != nil {
		name := r.Name.ToFHIR()
		if name.Text != "" || name.Family != "" || len(name.Prefix) > 0 || len(name.Given) > 0 {
			fhirData.Name = append(fhirData.Name, name)
		}
	}

	return fhirData
}

func (r PractitionerFHIR) ToAPISpec() Author {
	authorData := Author{}
	authorData.Aid = r.ID
	if len(r.Name) > 0 {
		name := r.Name[0].ToAPISpec()
		authorData.Name = &name
	}

	return authorData
}
