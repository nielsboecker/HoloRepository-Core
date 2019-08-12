import PipelinesService from "./pipelines.service";
import { Request, Response } from "express";
import samplePipelines from "../../../__tests__/samples/internal/samplePipelines.json";

export class ImagingStudiesController {
  public getAll(req: Request, res: Response): void {
    // Note: Once the HoloPipelines are ready, delete next line and uncomment the one after that
    res.json(samplePipelines);
    // res.redirect(308, PipelinesService.getPipelinesURL());
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

export default new ImagingStudiesController();
