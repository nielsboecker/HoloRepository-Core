import {
  IAddress,
  IHumanName,
  IImagingStudySeries,
  IPatient,
  IPerson,
  IPractitioner
} from "../../../../HoloRepositoryUI-Types";
import { R4 } from "@Ahryman40k/ts-fhir-types";
import { SupportedFhirResourceType } from "../clients/fhirClient";
import logger from "../logger";

const _normaliseDateString = (dateString: string): string => {
  // Note: Skipping validation of whether input string represents a date correctly
  const date = new Date(dateString);
  date.setUTCHours(0, 0, 0, 0);
  return date.toISOString();
};

const _mapHumanName = (names?: R4.IHumanName[]): IHumanName => {
  const name = names && names[0] ? names[0] : null;

  const given = name && name.given ? name.given.join(" ") : "";
  const family = name && name.family ? name.family : "Unknown";
  const full = `${given} ${family}`;
  const title = name && name.prefix && name.prefix[0] ? name.prefix[0] : "";

  return { given, family, full, title };
};

function _extractPhone(telecom?: R4.IContactPoint[]): string | undefined {
  if (telecom && telecom.find(tel => tel.system === R4.ContactPointSystemKind._phone)) {
    return telecom.find(tel => tel.system === R4.ContactPointSystemKind._phone).value;
  }
  return undefined;
}

function _extractAddress(address?: R4.IAddress[]): IAddress | undefined {
  return (
    address &&
    address[0] && {
      city: address[0].city,
      postcode: address[0].postalCode,
      state: address[0].state,
      street: address[0].line && address[0].line[0]
    }
  );
}

const _mapPerson = (person: R4.IPatient | R4.IPractitioner): IPerson | null => {
  // Note: Given the nature of FHIR, all of these fields may be undefined
  const { address, telecom, birthDate, gender, id, name, photo } = person;

  return {
    pid: id,
    name: name && _mapHumanName(name),
    gender: gender,
    birthDate: birthDate && _normaliseDateString(birthDate),
    phone: _extractPhone(telecom),
    address: _extractAddress(address),
    pictureUrl: photo && photo[0] && photo[0].url
  };
};

const _mapPatient = (patient: R4.IPatient): IPatient | null => {
  return _mapPerson(patient);
};

const _mapPractitioner = (practitioner: R4.IPractitioner): IPractitioner | null => {
  return _mapPerson(practitioner);
};

function _mapImagingStudySubject(is: R4.IImagingStudy) {
  let pid = undefined;
  let name = undefined;
  // Note: Azure FHIR server doesn't support "_include" queries yet, so in order to avoid a
  // second query, extract the PID from the reference string instead and omit name
  if (is.subject && is.subject.reference) {
    const uidParts = is.subject.reference.split("/");
    pid = uidParts[uidParts.length - 1];
  }

  return { pid, name };
}

const _extractEndpoint = (is: R4.IImagingStudy): string => {
  // Note: This is slightly hacky, a cleaner approach would use FhirClient.resolve();
  // this however would require another async call to the client. The given solution
  // is acceptable as we know that the endpoint is always the first contained resource.
  const endpoint: R4.IEndpoint = is.contained && is.contained[0] as R4.IEndpoint;
  return endpoint.address;
};

const _extractImagingStudySeriesPreviewUrl = (is: R4.IImagingStudy): string => {
  return `${_extractEndpoint(is)}.preview.jpg`;
};


const _mapImagingStudySeries = (
  is: R4.IImagingStudy
): IImagingStudySeries | undefined => {
  const { modality, id, started, series } = is;
  const iss = series && series[0] ? series[0] : null;

  return {
    bodySite: iss && iss.bodySite && iss.bodySite.display ? iss.bodySite.display : undefined,
    date: started ? _normaliseDateString(started) : undefined,
    issid: id ? id : undefined,
    modality:
      modality && modality[0] && modality[0].display
        ? modality[0].display
        : iss.modality && iss.modality.display
        ? iss.modality.display
        : undefined,
    numberOfInstances: iss.numberOfInstances ? iss.numberOfInstances : undefined,
    subject: _mapImagingStudySubject(is),
    endpoint: _extractEndpoint(is),
    previewPictureUrl: _extractImagingStudySeriesPreviewUrl(is)
  };
};

const getAdapterFunction = (resourceType: string): Function => {
  logger.debug(`Mapping type '${resourceType}'`);

  const { Patient, ImagingStudySeries, Practitioner } = SupportedFhirResourceType;
  switch (resourceType) {
    case Patient:
      return _mapPatient;
    case Practitioner:
      return _mapPractitioner;
    case ImagingStudySeries:
      return _mapImagingStudySeries;
    default:
      throw new Error(`Type not supported: ${resourceType}`);
  }
};

export { getAdapterFunction, _normaliseDateString };
