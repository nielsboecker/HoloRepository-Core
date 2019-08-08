import HologramsService from "./holograms.service";
import { Request, Response } from "express";

export class HologramsController {
  public async getAll(req: Request, res: Response): Promise<void> {
    res.redirect(308, HologramsService.getAllForPatientsURL(req.query.pids));
  }

  public downloadById(req: Request, res: Response): void {
    res.redirect(308, HologramsService.getDownloadURL(req.params.hid));
  }

  public deleteById(req: Request, res: Response): void {
    res.redirect(308, HologramsService.getEndpointURL(req.params.hid));
  }

  public upload(req: Request, res: Response): void {
    // Note: Ideally, the request should be checked for validity
    // Note: Upload models goes directly to the POST /holograms of HoloStorageAccessor
    res.redirect(308, HologramsService.getBaseURL());
  }

  public generate(req: Request, res: Response): void {
    // Note: Ideally, the request should be checked for validity
    // Note: Upload models goes directly to the POST /job of HoloPipelines
    res.redirect(308, HologramsService.getPipelineJobURL());
  }
}

export default new HologramsController();
