import { Router } from "express";
import PipelinesController from "./pipelines.controller";

const PipelinesRouter = Router()
  .get("/", PipelinesController.getAll)
  .get("/:jid/status", PipelinesController.getStatus)
  .post("/generate", PipelinesController.generate);

export default PipelinesRouter;
