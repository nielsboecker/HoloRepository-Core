import logger from "../../common/logger";
import PractitionersService from "../services/practitioners.service";
import { Request, Response } from "express";

export class ImagingStudiesController {
  all(req: Request, res: Response): void {
    PractitionersService.all().then(r => res.json(r));
  }

  byId(req: Request, res: Response): void {
    PractitionersService.byId(req.params.id).then(r => {
      if (r) res.json(r);
      else res.status(404).end();
    });
  }

  create(req: Request, res: Response): void {
    PractitionersService.create(req.body.name).then(r =>
      res
        .status(201)
        .location(`/api/v1/examples/${r.id}`)
        .json(r)
    );
  }
}
export default new ImagingStudiesController();
