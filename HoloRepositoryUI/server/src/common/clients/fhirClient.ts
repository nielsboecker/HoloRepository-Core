import Client from "fhir-kit-client";
import t from "io-ts";
import { decode, isDecodeError } from "io-ts-promise";
import { getAdapterFunction } from "../adapters/fhirAdapter";
import { R4 } from "@ahryman40k/ts-fhir-types";
import { IImagingStudy, IPatient, IPractitioner } from "../../../../types";
import logger from "../logger";

const { FHIR_SERVER_BASE_URL: fhirUrl } = process.env;

const _fhirClient = new Client({
  baseUrl: fhirUrl
});

export type InternalType = IPatient | IPractitioner | IImagingStudy;
export type SupportedFhirResource = R4.IPatient | R4.IPractitioner | R4.IImagingStudy;
export enum SupportedFhirResourceType {
  Patient = "Patient",
  Practitioner = "Practitioner",
  ImagingStudy = "ImagingStudy"
}

/**
 * Returns an io-ts decoder to validate a FHIR resource complies with the FHIR R4 definitions.
 * Note: ts-ignores are needed because we manually guarantee the right decoder for given type.
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
    case SupportedFhirResourceType.ImagingStudy:
      // @ts-ignore
      return R4.RTTI_ImagingStudy;
    default:
      throw new Error(`Type not supported: ${resourceType}`);
  }
};

/**
 * Handles errors occurring while fetching data from FHIR server and decoding them to the appropriate
 * types with io-ts. Outputs according error messages.
 */
const handleErrorWhileFetchingData = (error: Error) => {
  if (isDecodeError(error)) {
    logger.warn("Type decoding failed due to invalid data", error.message);
  } else {
    logger.warn("Request failed due to network issues", error.message);
  }
  return null;
};

/**
 * Handles errors occurring while mapping data to internal types. Outputs according error messages.
 */
const handleErrorWhileMappingData = (error: Error, context: string) => {
  logger.warn(`There was a problem while mapping data [${context}]`, error.message);
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
  logger.debug(`Fetching FHIR resource [${resourceType}/${id}]`);

  return _fhirClient
    .read({ resourceType, id })
    .then(decode(_getDecoder(resourceType)))
    .catch(handleErrorWhileFetchingData);
};

/**
 * Retrieves all FHIR resources of a resource type. The received FHIR Bundle gets unpacked
 * and all separate entries are being decoded.
 * @private
 */
const _getAllResources = async <Resource extends SupportedFhirResource>(
  resourceType: string,
  searchParams: object = {}
): Promise<Resource[]> => {
  logger.debug(`Fetching all FHIR resources [${resourceType}]`);

  const bundle: R4.IBundle = await _fhirClient
    .resourceSearch({
      resourceType,
      searchParams
    })
    .then(decode(R4.RTTI_Bundle))
    .catch(handleErrorWhileFetchingData);

  if (!bundle || !bundle.entry || bundle.entry.length === 0) {
    logger.warn(`Empty FHIR bundle for request [GET /${resourceType}/]`);
    return Promise.resolve([]);
  }

  const decoder = _getDecoder<Resource>(resourceType);
  const items = bundle.entry.map(item => item.resource).map(decode(decoder));

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
    .catch((error: Error) => handleErrorWhileMappingData(error, `GET ${resourceType}/${pid}`));
};

/**
 * Retrieves all FHIR resources of a resource type and maps them to the internal data type.
 *
 * @param resourceType  FHIR resource type
 * @param searchParams  optional set of search params to specify query
 */
const getAllAndMap = async <Resource extends SupportedFhirResource, Output extends InternalType>(
  resourceType: string,
  searchParams: object = {}
): Promise<Output[]> => {
  const map = getAdapterFunction(resourceType);
  return _getAllResources<Resource>(resourceType, searchParams)
    .then(resources => resources.map(resource => map(resource)))
    .catch((error: Error) => handleErrorWhileMappingData(error, `GET /${resourceType}/`));
};

export default { getAndMap, getAllAndMap };
