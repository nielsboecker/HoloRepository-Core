import { Router } from "express";
import PipelinesController from "../controllers/pipelines.controller";

const PipelinesRouter = Router().get("/", PipelinesController.getAll);

export default PipelinesRouter;
