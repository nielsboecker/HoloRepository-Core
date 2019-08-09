import { IHologram, IImagingStudy } from "./Holograms";

/**
 * Type representing a person's gener.
 * Semantics is similar to the corresponding FHIR resource.
 */
export type Gender = "male" | "female" | "other" | "unknown";

/**
 * Interface representing a person's name.
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
 * Interface representing a person's address.
 * Semantics is similar to the corresponding FHIR resource.
 */
export interface IAddress {
  street?: string;
  city?: string;
  state?: string;
  postcode?: string | number;
}

/**
 * Common attributes of Patients and Practitioners.
 * Semantics is similar to the corresponding FHIR resource.
 */
export interface IPerson {
  pid: string;
  name: IHumanName;
  gender: Gender;
  birthDate?: string;
  phone?: string;
  email?: string;
  address?: IAddress;
  pictureUrl?: string;
}

/**
 * Interface representing a Practitioner, the user of the system.
 * Semantics is similar to the corresponding FHIR resource.
 */
export interface IPractitioner extends IPerson {}

/**
 * Interface representing the subjects of the system.
 * Semantics is similar to the corresponding FHIR resource.
 */
export interface IPatient extends IPerson {
  imagingStudies?: IImagingStudy[];
  holograms?: IHologram[];
}
