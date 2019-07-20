import { IImagingStudySeries, IPatient, IPractitioner } from "../../../../HoloRepositoryUI-Types";
import { R4 } from "@Ahryman40k/ts-fhir-types";
import { SupportedFhirResourceType } from "../clients/fhirClient";
import logger from "../logger";

const _mapPatient = (patient: R4.IPatient): IPatient | null => {
 return {
    birthDate: patient.birthDate,
    gender: patient.gender,
    name: {
      full: patient.name[0].family
    },
    pid: patient.id
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
