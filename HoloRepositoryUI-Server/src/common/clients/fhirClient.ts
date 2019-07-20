import Client from "fhir-kit-client";
import t from "io-ts";
import * as tPromise from "io-ts-promise";
import { getAdapterFunction } from "../adapters/fhirAdapter";
import { FHIR_SERVER_BASE_URL } from "../../config";
import { R4 } from "@Ahryman40k/ts-fhir-types";
import { IImagingStudySeries, IPatient, IPractitioner } from "../../../../HoloRepositoryUI-Types";
import logger from "../logger";

const _fhirClient = new Client({
  baseUrl: FHIR_SERVER_BASE_URL
});

export type InternalType = IPatient | IPractitioner | IImagingStudySeries;
export type SupportedFhirResource = R4.IPatient | R4.IPractitioner | R4.IImagingStudy;
export enum SupportedFhirResourceType {
  Patient = "Patient",
  Practitioner = "Practitioner",
  // Note: We assume that there is just one series per study
  ImagingStudySeries = "ImagingStudy"
}

/**
 * Get an io-ts decoder to validate a FHIR resource complies with the FHIR R4 definitions.
 * @private
 */
const _getDecoder = (resourceType: string): t.Decoder<unknown, R4.IDomainResource> => {
  logger.debug(`Decoding type '${resourceType}'`);

  switch (resourceType) {
    case SupportedFhirResourceType.Patient:
      return R4.RTTI_Patient;
    case SupportedFhirResourceType.Practitioner:
      return R4.RTTI_Practitioner;
    case SupportedFhirResourceType.ImagingStudySeries:
      return R4.RTTI_ImagingStudy;
    default:
      throw new Error(`Type not supported: ${resourceType}`);
  }
};

/**
 * Generic method to retreive a FHIR resource by ID.
 * @private
 */
const _getResource = async <T extends SupportedFhirResource>(
  resourceType: string,
  id: string
): Promise<T> => {
  logger.debug(`Fetching FHIR resource '${resourceType}/${id}'`);

  return await _fhirClient
    .read({ resourceType, id })
    .then(tPromise.decode(_getDecoder(resourceType)))
    .catch((error: Error) => {
      if (tPromise.isDecodeError(error)) {
        logger.warn("Type decoding failed due to invalid data.", error.message);
      } else {
        logger.warn("Request failed due to network issues.", error.message);
      }
      return null;
    });
};

/**
 * Generic method to retreive a FHIR resource by ID and map it to the internal data type.
 * @private
 */
const _getAndMap = async <Resource extends SupportedFhirResource, Type extends InternalType>(
  resourceType: string,
  pid: string
): Promise<Type> => {
  const map = getAdapterFunction(resourceType);
  return _getResource<Resource>(resourceType, pid)
    .then(resource => map(resource))
    .catch((error: Error) => {
      logger.warn("Error while mapping data", error);
      return null;
    });
};

const getPatient = async (pid: string): Promise<IPatient> => {
  return _getAndMap<R4.IPatient, IPatient>("Patient", pid);
};

const getPractitioner = async (pid: string): Promise<IPractitioner> => {
  return _getAndMap<R4.IPractitioner, IPractitioner>("Practitioner", pid);
};

const getImagingStudySeries = async (issid: string): Promise<IImagingStudySeries> => {
  return _getAndMap<R4.IImagingStudy, IImagingStudySeries>(
    SupportedFhirResourceType.ImagingStudySeries,
    issid
  );
};

export { getPatient, getPractitioner, getImagingStudySeries };
