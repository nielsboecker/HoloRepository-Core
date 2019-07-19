import Client from "fhir-kit-client";
import { IPatient } from "../../../../HoloRepositoryUI-Types";
import { FhirResource, getAdapter } from "../adapters/fhirAdapter";
import { FHIR_SERVER_BASE_URL } from "../../config";

const fhirClient = new Client({
  baseUrl: FHIR_SERVER_BASE_URL
});

const getPatient = async (): Promise<IPatient | null> => {
  // Read a patient
  const pid = "e13d1464-d401-4be4-8b90-e8edadd6dce1";
  const adapter = getAdapter(FhirResource.Patient);
  return await fhirClient
    .read({ resourceType: "Patient", id: pid })
    .then(resource => adapter(resource));
};

export { fhirClient, getPatient };
