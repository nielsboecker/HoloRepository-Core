import Client from "fhir-kit-client";
import * as tPromise from "io-ts-promise";
import { FhirResource, getAdapter } from "../adapters/fhirAdapter";
import { FHIR_SERVER_BASE_URL } from "../../config";
import { R4 } from "@Ahryman40k/ts-fhir-types";
import { IPatient } from "../../../../HoloRepositoryUI-Types";

const fhirClient = new Client({
  baseUrl: FHIR_SERVER_BASE_URL
});

const getPatient = async (): Promise<IPatient | null> => {
  const pid = "e13d1464-d401-4be4-8b90-e8edadd6dce1xxxxx";
  const adapter = getAdapter(FhirResource.Patient);
  return await fhirClient
    .read({ resourceType: "Patient", id: pid })
    .then(tPromise.decode(R4.RTTI_Patient))
    .then(resource => adapter(resource))
    .catch((error: Error) => {
      if (tPromise.isDecodeError(error)) {
        console.error("Request failed due to invalid data.", error.message);
      } else {
        console.error("Request failed due to network issues.", error.message);
      }
    });
};

export { fhirClient, getPatient };
