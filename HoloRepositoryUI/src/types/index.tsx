interface PersonName {
  title: string;
  first: string[];
  last: string;
  full?: string;
}

/**
 * Common attributes of Patients and Practitioners.
 * Semantics is similar to the corresponding FHIR resource.
 */
interface Person {
  id: string;
  name: PersonName;
  email?: string;
  phone: string;
  dateOfBirth: string;
  address?: {
    street: string;
    city: string;
    state: string;
    postcode: string | number;
  };
  pictureUrl?: string;
}

/**
 * Interface representing the users of the system.
 * Semantics is similar to the corresponding FHIR resource, apart from the "patients" attribute.
 */
export interface Practitioner extends Person {
  patients: Patient[];
}

/**
 * Interface representing the subjects of the system.
 * Semantics is similar to the corresponding FHIR resource.
 */
export interface Patient extends Person {
  imagingStudySeries?: ImagingStudySeries[];
  holograms?: Hologram[];
}

/**
 * Interface representing one image series in a DICOM imaging study.
 * Semantics is similar to the corresponding FHIR resource.
 */
export interface ImagingStudySeries {
  id: string;
  subject: {
    id: string;
    name?: PersonName;
  };
  previewPictureUrl?: string;
  modality?: string;
  description?: string;
  bodySite?: string;
}

/**
 * Interface for a Hologram. Note that, similar to FHIR's ImagingStudy, the actual
 * binary data is not included, just an endpoint where it can be retreived.
 */
export interface Hologram {
  id: string;
  endpoint: string;
  title: string;
  subject: {
    id: string;
    name?: PersonName;
  };
  author: {
    id: string;
    name?: string;
  };
  createdAtDate?: string;
  fileSizeInKb?: number;
  imagingStudySeriesId?: string;
  // annotations?: Annotation[];
}

/**
 * Placeholder. Could be used for Annotator integration.
 */
interface Annotation {
  // Intentionally left blank
}
