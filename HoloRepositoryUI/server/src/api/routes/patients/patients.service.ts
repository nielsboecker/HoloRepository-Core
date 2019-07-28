import logger from "../../../common/logger";
import { IPatient } from "../../../../../HoloRepositoryUI-Types";
import { getAllPatients, getAllForPractitioner, getPatient } from "../../../common/data.service";

export class PatientsService {
  public getAll(): Promise<IPatient[]> {
    logger.info("GET all Patients");
    return getAllPatients();
  }

  public getAllForPractitioner(practitionerId: string): Promise<IPatient[]> {
    logger.info(`GET all Patients for general practitioner '${practitionerId}'`);
    return getAllForPractitioner(practitionerId);
  }

  public getById(pid: string): Promise<IPatient> {
    logger.info(`GET Patient by id '${pid}'`);
    return getPatient(pid);
  }
}

export default new PatientsService();
