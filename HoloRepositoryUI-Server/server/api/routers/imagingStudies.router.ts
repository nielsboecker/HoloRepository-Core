import { Router } from "express";
import controller from "../controllers/imagingStudies.controller";

const ImagingStudiesRouter = Router()
  .get("/", controller.getAll)
  .get("/:issid", controller.getById);

export default ImagingStudiesRouter;
