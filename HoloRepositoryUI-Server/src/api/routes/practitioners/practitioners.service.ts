import logger from "../../../common/logger";
import { IPractitioner } from "../../../../../HoloRepositoryUI-Types";

import samplePractitioner from "../../../__tests__/samples/samplePractitioner.json";

export class PractitionersService {
  public getById(pid: string): Promise<IPractitioner> {
    logger.info(`GET Practitioner by id '${pid}'`);
    return Promise.resolve(samplePractitioner as IPractitioner);
  }
}

export default new PractitionersService();
