import { R4 } from "@ahryman40k/ts-fhir-types";
import FhirClient, { SupportedFhirResourceType } from "./clients/fhirClient";
import { IImagingStudy, IPatient, IPractitioner } from "../../../HoloRepositoryUI-Types";

const getPatient = async (pid: string): Promise<IPatient> => {
  return FhirClient.getAndMap<R4.IPatient, IPatient>(SupportedFhirResourceType.Patient, pid);
};

const getAllPatients = async (): Promise<IPatient[]> => {
  return FhirClient.getAllAndMap<R4.IPatient, IPatient>(SupportedFhirResourceType.Patient);
};

const getAllForPractitioner = async (practitionerId: string): Promise<IPatient[]> => {
  return FhirClient.getAllAndMap<R4.IPatient, IPatient>(SupportedFhirResourceType.Patient, {
    "general-practitioner": practitionerId
  });
};

const getPractitioner = async (pid: string): Promise<IPractitioner> => {
  return FhirClient.getAndMap<R4.IPractitioner, IPractitioner>(
    SupportedFhirResourceType.Practitioner,
    pid
  );
};

const getImagingStudy = async (isid: string): Promise<IImagingStudy> => {
  return FhirClient.getAndMap<R4.IImagingStudy, IImagingStudy>(
    SupportedFhirResourceType.ImagingStudy,
    isid
  );
};

const getAllImagingStudies = async (): Promise<IImagingStudy[]> => {
  return FhirClient.getAllAndMap<R4.IImagingStudy, IImagingStudy>(
    SupportedFhirResourceType.ImagingStudy
  );
};

const getImagingStudiesForPatient = async (pid: string): Promise<IImagingStudy[]> => {
  return FhirClient.getAllAndMap<R4.IImagingStudy, IImagingStudy>(
    SupportedFhirResourceType.ImagingStudy,
    { patient: pid }
  );
};

export {
  getPatient,
  getAllPatients,
  getAllForPractitioner,
  getPractitioner,
  getImagingStudy,
  getAllImagingStudies,
  getImagingStudiesForPatient
};
