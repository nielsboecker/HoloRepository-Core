import HologramsService from "./holograms.service";
import { Request, Response } from "express";

export class HologramsController {
  public async getAll(req: Request, res: Response): Promise<void> {
    res.redirect(307, HologramsService.getAllForPatientsURL(req.query.pids));
  }

  public downloadById(req: Request, res: Response): void {
    res.redirect(307, HologramsService.getDownloadURL(req.params.hid));
  }

  public deleteById(req: Request, res: Response): void {
    res.redirect(307, HologramsService.getEndpointURL(req.params.hid));
  }

  public upload(req: Request, res: Response): void {
    // Note: Ideally, the request should be checked for validity
    // Note: Upload models goes directly to the POST /holograms of HoloStorageAccessor
    res.redirect(307, HologramsService.getBaseURL());
  }
}

export default new HologramsController();
