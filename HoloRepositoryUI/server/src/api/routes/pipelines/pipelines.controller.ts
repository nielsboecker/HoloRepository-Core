import PipelinesService from "./pipelines.service";
import { Request, Response } from "express";

export class ImagingStudiesController {
  public getAll(req: Request, res: Response): void {
    PipelinesService.getAll().then(pipelines => res.json(pipelines));
  }
}

export default new ImagingStudiesController();
