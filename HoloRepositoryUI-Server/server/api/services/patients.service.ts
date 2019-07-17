import logger from "../../common/logger";
import { IPatient } from "../../../../HoloRepositoryUI-Types";

import samplePatients from "../../../test/samples/samplePatients.json";

const _samplePatients = samplePatients as IPatient[];

export class PatientsService {
  public getAll(): Promise<IPatient[]> {
    logger.info("GET all Patients");
    return Promise.resolve(_samplePatients);
  }

  public getById(pid: string): Promise<IPatient> {
    logger.info(`GET Patient by id '${pid}'`);
    const patient = samplePatients.find(patient => patient.pid === pid);
    if (patient) {
      return Promise.resolve(patient as IPatient);
    }
  }
}

export default new PatientsService();
