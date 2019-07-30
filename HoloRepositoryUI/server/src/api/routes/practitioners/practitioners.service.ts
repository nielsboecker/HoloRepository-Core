import logger from "../../../common/logger";
import { IPractitioner } from "../../../../../types";
import { getPractitioner } from "../../../common/data.service";

export class PractitionersService {
  public getById(pid: string): Promise<IPractitioner> {
    logger.info(`GET Practitioner by id '${pid}'`);
    return getPractitioner(pid);
  }
}

export default new PractitionersService();
