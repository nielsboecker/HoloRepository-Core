import logger from "../../common/logger";
import { Router } from "express";
import controller from "../controllers/practitioners.controller";

const PractitionersRouter = Router()
  .post("/", controller.create)
  .get("/", controller.all)
  .get("/:id", controller.byId);

export default PractitionersRouter;
