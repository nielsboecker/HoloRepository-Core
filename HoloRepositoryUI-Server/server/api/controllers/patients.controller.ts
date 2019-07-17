import logger from "../../common/logger";
import PatientsService from "../services/patients.service";
import { Request, Response } from "express";

export class ImagingStudiesController {
  all(req: Request, res: Response): void {
    PatientsService.all().then(r => res.json(r));
  }

  byId(req: Request, res: Response): void {
    PatientsService.byId(req.params.id).then(r => {
      if (r) res.json(r);
      else res.status(404).end();
    });
  }

  create(req: Request, res: Response): void {
    PatientsService.create(req.body.name).then(r =>
      res
        .status(201)
        .location(`/api/v1/examples/${r.id}`)
        .json(r)
    );
  }
}
export default new ImagingStudiesController();
