import logger from "../../common/logger";
import { Router } from "express";
import controller from "../controllers/imagingStudies.controller";

const ImagingStudiesRouter = Router()
  .post("/", controller.create)
  .get("/", controller.all)
  .get("/:id", controller.byId);

export default ImagingStudiesRouter;
