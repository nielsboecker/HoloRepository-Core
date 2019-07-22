import logger from "../../../common/logger";
import { IPatient } from "../../../../../HoloRepositoryUI-Types";
import { getPatient } from "../../../common/data.service";

import samplePatientsAll from "../../../__tests__/samples/internal/samplePatientsAll.json";

const _samplePatients = samplePatientsAll as IPatient[];

export class PatientsService {
  public getAll(): Promise<IPatient[]> {
    logger.info("GET all Patients");
    return Promise.resolve(_samplePatients);
  }

  public getById(pid: string): Promise<IPatient> {
    logger.info(`GET Patient by id '${pid}'`);
    return getPatient(pid);
  }
}

export default new PatientsService();
