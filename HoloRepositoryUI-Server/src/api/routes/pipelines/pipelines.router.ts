import { Router } from "express";
import PipelinesController from "./pipelines.controller";

const PipelinesRouter = Router().get("/", PipelinesController.getAll);

export default PipelinesRouter;
