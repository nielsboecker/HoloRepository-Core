import logger from "../../common/logger";
import { Router } from "express";
import controller from "../controllers/pipelines.controller";

const PipelinesRouter = Router()
  .post("/", controller.create)
  .get("/", controller.all)
  .get("/:id", controller.byId);

export default PipelinesRouter;
