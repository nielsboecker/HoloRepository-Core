import { IHologram, IImagingStudySeries } from "./Holograms";

export const unknownPersonName = "Unknown";

export type Gender = "male" | "female" | "other" | "unknown";

/**
 * Interface representing a human name.
 * Semantics is similar to the corresponding FHIR resource; however, the structure
 * here is purposefully kept much simpler to avoid unnecessary complexity.
 */
export interface IHumanName {
  full: string;
  title?: string;
  given?: string;
  family?: string;
}

/**
 * Common attributes of Patients and Practitioners.
 * Semantics is similar to the corresponding FHIR resource.
 */
interface IPerson {
  id: string;
  name: IHumanName;
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
  patients?: IPatient[];
}

/**
 * Interface representing the subjects of the system.
 * Semantics is similar to the corresponding FHIR resource.
 */
export interface IPatient extends IPerson {
  imagingStudySeries?: IImagingStudySeries[];
  holograms?: IHologram[];
}
