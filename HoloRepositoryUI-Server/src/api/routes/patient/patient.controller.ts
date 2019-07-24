import PatientsService from "./patient.service";
import { Request, Response } from "express";

export class ImagingStudiesController {
  public getAll(req: Request, res: Response): void {
    const { practitioner } = req.query;

    if (practitioner) {
      PatientsService.getAllForPractitioner(practitioner).then(patients => res.json(patients));
    } else {
      PatientsService.getAll().then(patient => res.json(patient));
    }
  }

  public getById(req: Request, res: Response): void {
    PatientsService.getById(req.params.pid).then(patients => {
      if (patients) res.json(patients);
      else res.status(404).end();
    });
  }
}
export default new ImagingStudiesController();
