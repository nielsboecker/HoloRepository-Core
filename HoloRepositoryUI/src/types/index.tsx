export const UNKNOWN_PERSON_NAME = "Unknown";

interface IPersonName {
  full: string;
  title?: string;
  first?: string;
  last?: string;
}

type Gender = "male" | "female" | "other";

/**
 * Common attributes of Patients and Practitioners.
 * Semantics is similar to the corresponding FHIR resource.
 */
interface IPerson {
  id: string;
  name: IPersonName;
  gender: Gender;
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
export interface IPractitioner extends IPerson {
  patients: IPatient[];
}

/**
 * Interface representing the subjects of the system.
 * Semantics is similar to the corresponding FHIR resource.
 */
export interface IPatient extends IPerson {
  imagingStudySeries?: IImagingStudySeries[];
  holograms?: IHologram[];
}

/**
 * Interface representing one image series in a DICOM imaging study.
 * Semantics is similar to the corresponding FHIR resource.
 */
export interface IImagingStudySeries {
  id: string;
  subject: {
    id: string;
    name?: IPersonName;
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
export interface IHologram {
  id: string;
  endpoint: string;
  title: string;
  subject: {
    id: string;
    name?: IPersonName;
  };
  author: {
    id: string;
    name?: IPersonName;
  };
  createdDate: string;
  fileSizeInKb: number;
  imagingStudySeriesId?: string;
  // annotations?: IAnnotation[];
}

/**
 * Placeholder. Could be used for Annotator integration.
 */
interface IAnnotation {
  // Intentionally left blank
}
