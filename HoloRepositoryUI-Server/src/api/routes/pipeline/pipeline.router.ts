import { Router } from "express";
import PipelinesController from "./pipeline.controller";

const PipelineRouter = Router().get("/", PipelinesController.getAll);

export default PipelineRouter;
