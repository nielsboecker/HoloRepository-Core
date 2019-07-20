import {
  IImagingStudySeries,
  IPatient,
  IPractitioner,
  IHumanName
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

const _mapPatient = (patient: R4.IPatient): IPatient | null => {
  return {
    pid: patient.id || "unknown",
    name: _mapHumanName(patient.name),
    birthDate: patient.birthDate || "unknown",
    gender: patient.gender || "unknown"
  };
};

const _mapPractitioner = (practitioner: R4.IPractitioner): IPractitioner | null => {
  // TODO: Implement
  return null;
};

const _mapImagingStudySeries = (iss: R4.IImagingStudy): IImagingStudySeries | null => {
  // TODO: Implement
  return null;
};

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
