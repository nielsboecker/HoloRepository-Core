import logger from "../../../common/logger";
import { IPipeline } from "../../../../../HoloRepositoryUI-Types";

import samplePipelines from "../../../__tests__/samples/internal/samplePipelines.json";

export class PipelineService {
  public getAll(): Promise<IPipeline[]> {
    logger.info("GET all Pipelines");

    // Note: This will have to remain mocked until HoloPipelines endpoint is ready
    return Promise.resolve(samplePipelines as IPipeline[]);
  }
}

export default new PipelineService();
