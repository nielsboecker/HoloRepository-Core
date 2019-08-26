import PipelinesService from "./pipelines.service";
import { Request, Response } from "express";

export class PipelinesController {
  public getAll(req: Request, res: Response): void {
    res.redirect(307, PipelinesService.getPipelinesURL());
  }

  public getState(req: Request, res: Response): void {
    res.redirect(307, PipelinesService.getJobStateURL(req.params.jid));
  }

  public getLog(req: Request, res: Response): void {
    res.redirect(307, PipelinesService.getJobLogURL(req.params.jid));
  }

  public generate(req: Request, res: Response): void {
    // Note: Ideally, the request should be checked for validity
    // Note: Upload models goes directly to the POST /job of HoloPipelines
    res.redirect(307, PipelinesService.getJobsURL());
  }
}

export default new PipelinesController();
