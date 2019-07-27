import logger from "../../../common/logger";
import { IPractitioner } from "../../../../../HoloRepositoryUI-Types";
import { getPractitioner } from "../../../common/data.service";

export class PractitionersService {
  public getById(pid: string): Promise<IPractitioner> {
    logger.info(`GET Practitioner by id '${pid}'`);
    return getPractitioner(pid);
  }
}

export default new PractitionersService();
