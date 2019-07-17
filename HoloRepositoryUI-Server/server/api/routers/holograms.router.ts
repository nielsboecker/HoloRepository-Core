import logger from "../../common/logger";
import { Router } from "express";
import controller from "../controllers/holograms.controller";

const HologramsRouter = Router()
  .post("/", controller.create)
  .get("/", controller.all)
  .get("/:id", controller.byId);

export default HologramsRouter;
