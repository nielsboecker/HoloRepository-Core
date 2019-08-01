import HologramsService from "./holograms.service";
import { Request, Response } from "express";
import logger from "../../../common/logger";
import ImagingStudiesService from "../imagingStudies/imagingStudies.service";

export class HologramsController {
  public async getAll(req: Request, res: Response): Promise<void> {
    const { pids } = req.query;

    // Note: similar to getAll in ImagingStudyController, should be refactored
    if (pids) {
      const pidsSplit = pids.split(",");
      if (pidsSplit.length === 0) {
        logger.warn(`Cannot get all holograms for pids = '${pids}'`);
        res.status(400).end();
      } else {
        logger.info(`GET all holograms for pids = ${pidsSplit}`);
        const hologramsForPids = {};
        await Promise.all(
          pidsSplit.map(pid =>
            HologramsService.getAllForPatient(pid).then(
              hologram => (hologramsForPids[pid] = hologram)
            )
          )
        );
        res.json(hologramsForPids);
      }
    } else {
      ImagingStudiesService.getAll().then(iss => res.json(iss));
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
