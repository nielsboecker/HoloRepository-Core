import HologramsService from "./holograms.service";
import { Request, Response } from "express";
import getConditionalPidsFilter from "../../util/filter.util";
import logger from "../../../common/logger";

export class HologramsController {
  public getAll(req: Request, res: Response): void {
    HologramsService.getAll()
      .then(value => value.filter(getConditionalPidsFilter(req.query)))
      .then(holograms => res.json(holograms));
  }

  public getById(req: Request, res: Response): void {
    HologramsService.getById(req.params.hid).then(hologram => {
      if (hologram) res.json(hologram);
      else res.status(404).end();
    });
  }

  public downloadById(req: Request, res: Response): void {
    HologramsService.downloadById(req.params.hid).then(hologram => {
      if (hologram) res.send(hologram);
      else res.status(404).end();
    });
  }

  public deleteById(req: Request, res: Response): void {
    HologramsService.deleteById(req.params.hid).then(success => {
      if (success) res.status(200).end();
      else res.status(404).end();
    });
  }

  public upload(req: Request, res: Response): void {
    HologramsService.upload().then(success => {
      if (success) res.status(200).end();
      else res.status(404).end();
    });
  }

  public generate(req: Request, res: Response): void {
    HologramsService.generate().then(success => {
      if (success) res.status(200).end();
      else res.status(404).end();
    });
  }
}

export default new HologramsController();
