import HologramsService from "../services/holograms.service";
import { Request, Response } from "express";
import getConditionalPidsFilter from "../util/filter.util";
import logger from "../../common/logger";

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
    logger.warn("Download not implemented yet");
    res.status(500).end();
  }

  public deleteById(req: Request, res: Response): void {
    logger.warn("Delete not implemented yet");
    res.status(500).end();
  }
}

export default new HologramsController();
