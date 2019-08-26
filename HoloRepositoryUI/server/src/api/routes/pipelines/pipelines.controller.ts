import PipelinesService from "./pipelines.service";
import { Request, Response } from "express";

export class PipelinesController {
  public getAll(req: Request, res: Response): void {
    res.redirect(308, PipelinesService.getPipelinesURL());
  }

  public getStatus(req: Request, res: Response): void {
    res.redirect(308, PipelinesService.getJobStatusURL(req.params.jid));
  }

  public generate(req: Request, res: Response): void {
    // Note: Ideally, the request should be checked for validity
    // Note: Upload models goes directly to the POST /job of HoloPipelines
    res.redirect(308, PipelinesService.getJobURL());
  }
}

export default new PipelinesController();
