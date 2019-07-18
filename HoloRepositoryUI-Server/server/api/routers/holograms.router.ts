import { Router } from "express";
import HologramsController from "../controllers/holograms.controller";

const HologramsRouter = Router()
  .get("/", HologramsController.getAll)
  .get("/:hid", HologramsController.getById)
  .get("/:hid/download", HologramsController.downloadById)
  .delete("/:hid", HologramsController.deleteById);

export default HologramsRouter;
