import logger from "../../common/logger";
import HologramsService from "../services/holograms.service";
import { Request, Response } from "express";

export class ExamplesController {
  all(req: Request, res: Response): void {
    HologramsService.all().then(r => res.json(r));
  }

  byId(req: Request, res: Response): void {
    HologramsService.byId(req.params.id).then(r => {
      if (r) res.json(r);
      else res.status(404).end();
    });
  }

  create(req: Request, res: Response): void {
    HologramsService.create(req.body.name).then(r =>
      res
        .status(201)
        .location(`/api/v1/examples/${r.id}`)
        .json(r)
    );
  }
}
export default new ExamplesController();
