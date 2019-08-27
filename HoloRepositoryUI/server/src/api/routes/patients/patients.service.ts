import logger from "../../../common/logger";
import { IPatient } from "../../../../../types";
import FhirClient, { SupportedFhirResourceType } from "../../../common/clients/fhirClient";
import { R4 } from "@ahryman40k/ts-fhir-types";

export class PatientsService {
  public getAll(): Promise<IPatient[]> {
    logger.info("GET all Patients");
    return FhirClient.getAllAndMap<R4.IPatient, IPatient>(SupportedFhirResourceType.Patient);
  }

  public getAllForPractitioner(practitionerId: string): Promise<IPatient[]> {
    logger.info(`GET all Patients for general practitioner '${practitionerId}'`);
    return FhirClient.getAllAndMap<R4.IPatient, IPatient>(SupportedFhirResourceType.Patient, {
      "general-practitioner": practitionerId
    });
  }

  public getById(pid: string): Promise<IPatient> {
    logger.info(`GET Patient by id '${pid}'`);
    return FhirClient.getAndMap<R4.IPatient, IPatient>(SupportedFhirResourceType.Patient, pid);
  }
}

export default new PatientsService();
