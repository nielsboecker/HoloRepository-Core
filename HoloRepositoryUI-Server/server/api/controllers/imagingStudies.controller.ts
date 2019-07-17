import ImagingStudiesService from "../services/imagingStudies.service";
import { Request, Response } from "express";

export class ImagingStudiesController {
  public getAll(req: Request, res: Response): void {
    ImagingStudiesService.getAll().then(iss => res.json(iss));
  }

  public getById(req: Request, res: Response): void {
    ImagingStudiesService.getById(req.params.issid).then(iss => {
      if (iss) {
        res.json(iss);
      } else {
        res.status(404).end();
      }
    });
  }
}
export default new ImagingStudiesController();
