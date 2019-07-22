import logger from "../../common/logger";
import { IPatient } from "../../../../HoloRepositoryUI-Types";

import samplePatientsAll from "../../../test/samples/samplePatientsAll.json";

const _samplePatients = samplePatientsAll as IPatient[];

export class PatientsService {
  public getAll(): Promise<IPatient[]> {
    logger.info("GET all Patients");
    return Promise.resolve(_samplePatients);
  }

  public getById(pid: string): Promise<IPatient> {
    logger.info(`GET Patient by id '${pid}'`);
    const patient = samplePatientsAll.find(patient => patient.pid === pid);
    if (patient) {
      return Promise.resolve(patient as IPatient);
    }
  }
}

export default new PatientsService();
