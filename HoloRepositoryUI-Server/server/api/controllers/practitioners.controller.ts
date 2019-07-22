import PractitionersService from "../services/practitioners.service";
import { Request, Response } from "express";

export class PractitionersController {
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

export default new PractitionersController();
