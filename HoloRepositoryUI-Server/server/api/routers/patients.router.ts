import logger from "../../common/logger";
import { Router } from "express";
import controller from "../controllers/patients.controller";

const PatientsRouter = Router()
  .post("/", controller.create)
  .get("/", controller.all)
  .get("/:id", controller.byId);

export default PatientsRouter;
