import PipelinesService from "./pipelines.service";
import { Request, Response } from "express";
import logger from "../../../common/logger";

export class PipelinesController {
  public getAll(req: Request, res: Response): void {
    logger.info("GET pipelines");
    res.redirect(307, PipelinesService.getPipelinesURL());
  }

  public getState(req: Request, res: Response): void {
    const jid = req.params.jid;
    logger.info(`GET job state for '${jid}'`);
    res.redirect(307, PipelinesService.getJobStateURL(jid));
  }

  public getLog(req: Request, res: Response): void {
    const jid = req.params.jid;
    logger.info(`GET job log for '${jid}'`);
    res.redirect(307, PipelinesService.getJobLogURL(jid));
  }

  public generate(req: Request, res: Response): void {
    // Note: Ideally, the request should be checked for validity
    // Note: Upload models goes directly to the POST /job of HoloPipelines
    logger.info(`POST generate new hologram`);
    res.redirect(307, PipelinesService.getJobsURL());
  }
}

export default new PipelinesController();
