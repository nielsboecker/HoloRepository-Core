import Client from "fhir-kit-client";
import t from "io-ts";
import { decode, isDecodeError } from "io-ts-promise";
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
 * Returns an io-ts decoder to validate a FHIR resource complies with the FHIR R4 definitions.
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
 * Retrieves a FHIR resource by ID.
 * @private
 */
const _getResource = async <T extends SupportedFhirResource>(
  resourceType: string,
  id: string
): Promise<T> => {
  logger.debug(`Fetching FHIR resource '${resourceType}/${id}'`);

  return await _fhirClient
    .read({ resourceType, id })
    .then(decode(_getDecoder(resourceType)))
    .catch((error: Error) => {
      if (isDecodeError(error)) {
        logger.warn("Type decoding failed due to invalid data.", error.message);
      } else {
        logger.warn("Request failed due to network issues.", error.message);
      }
      return null;
    });
};

/**
 * Retrieves a FHIR resource by ID and maps it to the internal data type.
 */
const getAndMap = async <Resource extends SupportedFhirResource, Type extends InternalType>(
  resourceType: string,
  pid: string
): Promise<Type> => {
  const map = getAdapterFunction(resourceType);
  return _getResource<Resource>(resourceType, pid)
    .then(resource => map(resource))
    .catch((error: Error) => {
      logger.warn(`Error while mapping data [${resourceType}/${pid}]`, error);
      return null;
    });
};

export default { getAndMap };
