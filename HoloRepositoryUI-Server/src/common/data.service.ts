import { R4 } from "@ahryman40k/ts-fhir-types";
import FhirClient, { SupportedFhirResourceType } from "./clients/fhirClient";
import { IImagingStudySeries, IPatient, IPractitioner } from "../../../HoloRepositoryUI-Types";

const getPatient = async (pid: string): Promise<IPatient> => {
  return FhirClient.getAndMap<R4.IPatient, IPatient>(SupportedFhirResourceType.Patient, pid);
};

const getPractitioner = async (pid: string): Promise<IPractitioner> => {
  return FhirClient.getAndMap<R4.IPractitioner, IPractitioner>(
    SupportedFhirResourceType.Practitioner,
    pid
  );
};

const getImagingStudySeries = async (issid: string): Promise<IImagingStudySeries> => {
  return FhirClient.getAndMap<R4.IImagingStudy, IImagingStudySeries>(
    SupportedFhirResourceType.ImagingStudySeries,
    issid
  );
};

export { getPatient, getPractitioner, getImagingStudySeries };
