import { Router } from "express";
import controller from "../controllers/imagingStudySeries.controller";

const ImagingStudySeriesRouter = Router()
  .get("/", controller.getAll)
  .get("/:issid", controller.getById);

export default ImagingStudySeriesRouter;
