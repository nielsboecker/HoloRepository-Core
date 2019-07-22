import logger from "../../../common/logger";
import { IPatient } from "../../../../../HoloRepositoryUI-Types";
import { getAllPatients, getPatient } from "../../../common/data.service";

export class PatientsService {
  public getAll(): Promise<IPatient[]> {
    logger.info("GET all Patients");
    return getAllPatients();
  }

  public getById(pid: string): Promise<IPatient> {
    logger.info(`GET Patient by id '${pid}'`);
    return getPatient(pid);
  }
}

export default new PatientsService();
