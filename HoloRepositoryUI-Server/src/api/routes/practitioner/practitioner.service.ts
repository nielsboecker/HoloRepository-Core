import logger from "../../../common/logger";
import { IPractitioner } from "../../../../../HoloRepositoryUI-Types";
import { getPractitioner } from "../../../common/data.service";

export class PractitionerService {
  public getById(pid: string): Promise<IPractitioner> {
    logger.info(`GET Practitioner by id '${pid}'`);
    return getPractitioner(pid);
  }
}

export default new PractitionerService();
