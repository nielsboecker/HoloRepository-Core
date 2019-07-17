import { Router } from "express";
import PatientsController from "../controllers/patients.controller";

const PatientsRouter = Router()
  .get("/", PatientsController.getAll)
  .get("/:pid", PatientsController.getById);

export default PatientsRouter;
