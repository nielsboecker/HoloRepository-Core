import HologramsService from "./holograms.service";
import { Request, Response } from "express";

export class HologramsController {
  public async getAll(req: Request, res: Response): Promise<void> {
    const { pids } = req.query;

    if (pids) {
      HologramsService.getAllForPatients(pids).then(holograms => res.json(holograms));
    } else {
      res.json([]);
    }
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
