import HologramsService from "../services/holograms.service";
import { Request, Response } from "express";

export class HologramsController {
  public getAll(req: Request, res: Response): void {
    HologramsService.getAll().then(holograms => res.json(holograms));
  }

  public getById(req: Request, res: Response): void {
    HologramsService.getById(req.params.hid).then(hologram => {
      if (hologram) res.json(hologram);
      else res.status(404).end();
    });
  }
}
export default new HologramsController();
