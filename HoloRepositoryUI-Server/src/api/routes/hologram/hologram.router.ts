import { Router } from "express";
import HologramsController from "./hologram.controller";

const HologramRouter = Router()
  .get("/", HologramsController.getAll)
  .get("/:hid", HologramsController.getById)
  .get("/:hid/download", HologramsController.downloadById)
  .delete("/:hid", HologramsController.deleteById)
  .post("/upload", HologramsController.upload)
  .post("/generate", HologramsController.generate);

export default HologramRouter;
