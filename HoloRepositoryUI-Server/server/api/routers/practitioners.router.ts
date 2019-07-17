import { Router } from "express";
import PractitionersController from "../controllers/practitioners.controller";

const PractitionersRouter = Router().get("/:pid", PractitionersController.getById);

export default PractitionersRouter;
