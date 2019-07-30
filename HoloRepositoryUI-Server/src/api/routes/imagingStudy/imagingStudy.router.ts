import { Router } from "express";
import controller from "./imagingStudy.controller";

const ImagingStudyRouter = Router()
  .get("/", controller.getAll)
  .get("/:isid", controller.getById);

export default ImagingStudyRouter;
