import HologramsService from "./holograms.service";
import { Request, Response } from "express";

export class HologramsController {
  public async getAll(req: Request, res: Response): Promise<void> {
    res.redirect(HologramsService.getAllForPatientsURL(req.query.pids));
  }

  public downloadById(req: Request, res: Response): void {
    res.redirect(HologramsService.getDownloadURL(req.params.hid));
  }

  public deleteById(req: Request, res: Response): void {
    res.redirect(307, HologramsService.getEndpointURL(req.params.hid));
  }

  public upload(req: Request, res: Response): void {
    // Note: Ideally, the request should be checked for validity
    res.redirect(307, HologramsService.getBaseURL());
  }

  public generate(req: Request, res: Response): void {
    HologramsService.generate().then(success => {
      if (success) res.status(200).end();
      else res.status(404).end();
    });
  }
}

export default new HologramsController();
