import logger from "../../common/logger";
import { IPipeline } from "../../../../HoloRepositoryUI-Types";

import samplePipelines from "../../../test/samples/samplePipelines.json";

export class PipelinesService {
  public getAll(): Promise<IPipeline[]> {
    logger.info("GET all Pipelnes");
    return Promise.resolve(samplePipelines as IPipeline[]);
  }
}

export default new PipelinesService();
