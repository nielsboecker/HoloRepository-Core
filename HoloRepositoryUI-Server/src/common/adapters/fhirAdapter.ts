import {
  IImagingStudySeries,
  IPatient,
  IPractitioner,
  IHumanName,
  IPerson
} from "../../../../HoloRepositoryUI-Types";
import { R4 } from "@Ahryman40k/ts-fhir-types";
import { SupportedFhirResourceType } from "../clients/fhirClient";
import logger from "../logger";

const _mapHumanName = (names?: R4.IHumanName[]): IHumanName => {
  const name = names && names[0] ? names[0] : null;

  const given = name && name.given ? name.given.join(" ") : "";
  const family = name && name.family ? name.family : "Unknown";
  const full = `${given} ${family}`;
  const title = name && name.prefix && name.prefix[0] ? name.prefix[0] : "";

  return { given, family, full, title };
};

const _mapPerson = (person: R4.IPatient| R4.IPractitioner): IPerson | null => {
  return {
    pid: person.id || "unknown",
    name: _mapHumanName(person.name),
    birthDate: person.birthDate || "unknown",
    gender: person.gender || "unknown"
  };
};

const _mapPatient = (patient: R4.IPatient): IPatient | null => {
  return _mapPerson(patient);
};

const _mapPractitioner = (practitioner: R4.IPractitioner): IPractitioner | null => {
  return _mapPerson(practitioner);
};

const _mapImagingStudySeries = (iss: R4.IImagingStudy): IImagingStudySeries | null => ({
  bodySite: "",
  date: "",
  issid: "",
  modality: "",
  numberOfInstances: 0,
  previewPictureUrl: "",
  subject: { pid: "" }
});

const getAdapterFunction = (resourceType: string): Function => {
  logger.debug(`Mapping type '${resourceType}'`);

  switch (resourceType) {
    case SupportedFhirResourceType.Patient:
      return _mapPatient;
    case SupportedFhirResourceType.Practitioner:
      return _mapPractitioner;
    case SupportedFhirResourceType.ImagingStudySeries:
      return _mapImagingStudySeries;
    default:
      throw new Error(`Type not supported: ${resourceType}`);
  }
};

export { getAdapterFunction };
