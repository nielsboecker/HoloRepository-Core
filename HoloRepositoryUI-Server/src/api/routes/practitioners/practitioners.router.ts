import { Router } from "express";
import PractitionersController from "./practitioners.controller";

const PractitionersRouter = Router().get("/:pid", PractitionersController.getById);

export default PractitionersRouter;
