import logger from "../../../common/logger";
import { IPipeline } from "../../../../../HoloRepositoryUI-Types";

import samplePipelines from "../../../__tests__/samples/samplePipelines.json";

export class PipelinesService {
  public getAll(): Promise<IPipeline[]> {
    logger.info("GET all Pipelines");
    return Promise.resolve(samplePipelines as IPipeline[]);
  }
}

export default new PipelinesService();