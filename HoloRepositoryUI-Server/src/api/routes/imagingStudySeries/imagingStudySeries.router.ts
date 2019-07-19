import { Router } from "express";
import controller from "./imagingStudySeries.controller";

const ImagingStudySeriesRouter = Router()
  .get("/", controller.getAll)
  .get("/:issid", controller.getById)
  .get("/:issid/preview", controller.getPreviewById);

export default ImagingStudySeriesRouter;
