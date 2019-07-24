import { Router } from "express";
import PatientsController from "./patient.controller";

const PatientRouter = Router()
  .get("/", PatientsController.getAll)
  .get("/:pid", PatientsController.getById);

export default PatientRouter;
