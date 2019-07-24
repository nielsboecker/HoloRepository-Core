import { Router } from "express";
import PractitionersController from "./practitioner.controller";

const PractitionerRouter = Router().get("/:pid", PractitionersController.getById);

export default PractitionerRouter;
