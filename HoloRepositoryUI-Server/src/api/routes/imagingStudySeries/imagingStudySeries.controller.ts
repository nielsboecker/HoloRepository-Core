import ImagingStudiesService from "./imagingStudySeries.service";
import { Request, Response } from "express";
import logger from "../../../common/logger";

export class ImagingStudySeriesController {
  public getAll(req: Request, res: Response): void {
    const { pids } = req.query;

    if (pids) {
      const pidsSplit = pids.split(",");
      if (pidsSplit.length === 0) {
        logger.warn(`Cannot get all ImagingStudySeries for pids = '${pids}'`);
        res.status(400).end();
      } else {
        logger.info(`GET all ImagingStudySeries for pids = ${pidsSplit}`);
        const issForPids = {};
        pidsSplit.forEach(pid => {
          ImagingStudiesService.getAllForPatient(pid).then(iss => (issForPids[pid] = iss));
        });
        res.json(issForPids);
      }
    } else {
      ImagingStudiesService.getAll().then(iss => res.json(iss));
    }
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
