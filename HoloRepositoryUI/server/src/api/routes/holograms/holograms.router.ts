import { Router } from "express";
import HologramsController from "./holograms.controller";

const HologramsRouter = Router()
  .get("/", HologramsController.getAll)
  .get("/:hid/download", HologramsController.downloadById)
  .delete("/:hid", HologramsController.deleteById)
  .post("/upload", HologramsController.upload);

export default HologramsRouter;
