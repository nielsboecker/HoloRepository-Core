import PractitionersService from "./practitioner.service";
import { Request, Response } from "express";

export class PractitionerController {
  public getById(req: Request, res: Response): void {
    PractitionersService.getById(req.params.pid).then(practitioner => {
      if (practitioner) {
        res.json(practitioner);
      } else {
        res.status(404).end();
      }
    });
  }
}

export default new PractitionerController();
