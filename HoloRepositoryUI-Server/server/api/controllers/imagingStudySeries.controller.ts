import ImagingStudiesService from "../services/imagingStudySeries.service";
import { Request, Response } from "express";
import HologramsService from "../services/holograms.service";
import getConditionalPidsFilter from "../util/filter.util";

export class ImagingStudySeriesController {
  public getAll(req: Request, res: Response): void {
    ImagingStudiesService.getAll()
      .then(value => value.filter(getConditionalPidsFilter(req.query)))
      .then(iss => res.json(iss));
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
export default new ImagingStudySeriesController();
