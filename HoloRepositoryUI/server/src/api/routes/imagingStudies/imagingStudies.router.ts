import { Router } from "express";
import controller from "./imagingStudies.controller";

const ImagingStudiesRouter = Router()
  .get("/", controller.getAll)
  .get("/:isid", controller.getById);

export default ImagingStudiesRouter;
