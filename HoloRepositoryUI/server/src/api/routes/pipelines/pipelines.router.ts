import { Router } from "express";
import PipelinesController from "./pipelines.controller";

const PipelinesRouter = Router()
  .get("/", PipelinesController.getAll)
  .get("/:jid/state", PipelinesController.getState)
  .get("/:jid/log", PipelinesController.getLog)
  .post("/generate", PipelinesController.generate);

export default PipelinesRouter;
