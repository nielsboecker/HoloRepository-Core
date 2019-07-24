import logger from "../../../common/logger";
import { IPatient } from "../../../../../HoloRepositoryUI-Types";
import {
  getAllPatients,
  getAllForGeneralPractitioner,
  getPatient
} from "../../../common/data.service";

export class PatientService {
  public getAll(): Promise<IPatient[]> {
    logger.info("GET all Patients");
    return getAllPatients();
  }

  public getAllForGeneralPractitioner(generalPractitioner: string): Promise<IPatient[]> {
    logger.info(`GET all Patients for general practitioner '${generalPractitioner}'`);
    return getAllForGeneralPractitioner(generalPractitioner);
  }

  public getById(pid: string): Promise<IPatient> {
    logger.info(`GET Patient by id '${pid}'`);
    return getPatient(pid);
  }
}

export default new PatientService();
