import { Application, Router } from "express";
import examplesRouter from "./api/controllers/examples/router";
import PatientsRouter from "./api/routers/patients.router";
import PractitionersRouter from "./api/routers/practitioners.router";
import HologramsRouter from "./api/routers/holograms.router";
import PipelinesRouter from "./api/routers/pipelines.router";
import ImagingStudiesRouter from "./api/routers/imagingStudies.router";

const apiVersion = 1;
const apiPrefix = `/api/v${apiVersion}`;

const apiRouter = Router()
  .use("/patients", PatientsRouter)
  .use("/practitioners", PractitionersRouter)
  .use("/holograms", HologramsRouter)
  .use("/pipelines", PipelinesRouter)
  .use("/imagingStudies", ImagingStudiesRouter);

const routes = (app: Application): void => {
  app.use(apiPrefix, apiRouter);
};

export default routes;
