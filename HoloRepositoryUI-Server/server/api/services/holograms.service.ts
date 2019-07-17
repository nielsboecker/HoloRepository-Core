import logger from "../../common/logger";

export class HologramsService {
  all(): Promise<any[]> {
    logger.info("fetch all");
    return Promise.resolve([]);
  }

  byId(id: number): Promise<any> {
    logger.info(`fetch example with id ${id}`);
    return this.all().then(response => response[id]);
  }

  create(name: string): Promise<any> {
    logger.info(`create with name ${name}`);
    return Promise.resolve(null);
  }
}

export default new HologramsService();
