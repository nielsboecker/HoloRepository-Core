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
const _getDecoder = <Resource extends SupportedFhirResource>(
  resourceType: string
): t.Decoder<unknown, Resource> => {
  logger.debug(`Decoding type '${resourceType}'`);

  switch (resourceType) {
    case SupportedFhirResourceType.Patient:
      // @ts-ignore
      return R4.RTTI_Patient;
    case SupportedFhirResourceType.Practitioner:
      // @ts-ignore
      return R4.RTTI_Practitioner;
    case SupportedFhirResourceType.ImagingStudySeries:
      // @ts-ignore
      return R4.RTTI_ImagingStudy;
    default:
      throw new Error(`Type not supported: ${resourceType}`);
  }
};

/**
 * Handles errors and outputs according error messages.
 */
const handleError = (error: Error) => {
  if (isDecodeError(error)) {
    logger.warn("Type decoding failed due to invalid data.", error.message);
  } else {
    logger.warn("Request failed due to network issues.", error.message);
  }
  return null;
};

/**
 * Retrieves a FHIR resource by ID.
 * @private
 */
const _getResource = async <Resource extends SupportedFhirResource>(
  resourceType: string,
  id: string
): Promise<Resource> => {
  logger.debug(`Fetching FHIR resource '${resourceType}/${id}'`);

  return await _fhirClient
    .read({ resourceType, id })
    .then(decode(_getDecoder(resourceType)))
    .catch(handleError);
};

/**
 * Retrieves all FHIR resources of a resource type. The received FHIR Bundle gets unpacked
 * and all separate entries are being decoded.
 * @private
 */
const _getAllResources = async <Resource extends SupportedFhirResource>(
  resourceType: string
): Promise<Resource[]> => {
  logger.debug(`Fetching all FHIR resources '${resourceType}'`);

  const bundle: R4.IBundle = await _fhirClient
    .resourceSearch({
      resourceType,
      searchParams: {}
    })
    .then(decode(R4.RTTI_Bundle))
    .catch(handleError);

  const decoder = _getDecoder<Resource>(resourceType);
  const items = bundle.entry
    .map(item => item.resource)
    .map(decode(decoder));

  return Promise.all(items);
};

/**
 * Retrieves a FHIR resource by ID and maps it to the internal data type.
 */
const getAndMap = async <Resource extends SupportedFhirResource, Output extends InternalType>(
  resourceType: string,
  pid: string
): Promise<Output> => {
  const map = getAdapterFunction(resourceType);
  return _getResource<Resource>(resourceType, pid)
    .then(resource => map(resource))
    .catch((error: Error) => {
      logger.warn(`Error while mapping data [${resourceType}/${pid}]`, error);
      return null;
    });
};

/**
 * Retrieves all FHIR resource of a resource type and maps it to the internal data type.
 */
const getAllAndMap = async <Resource extends SupportedFhirResource, Output extends InternalType>(
  resourceType: string
): Promise<Output[]> => {
  const map = getAdapterFunction(resourceType);
  return _getAllResources<Resource>(resourceType)
  .then(resources => resources.map(resource => map(resource)))
  .catch((error: Error) => {
    logger.warn(`Error while mapping data [all ${resourceType}s]`, error);
    return null;
  });
};

export default { getAndMap, getAllAndMap };
