import { Application } from "express";
import PatientsRouter from "./api/routers/patients.router";
import HologramsRouter from "./api/routers/holograms.router";
import PipelinesRouter from "./api/routers/pipelines.router";
import ImagingStudiesRouter from "./api/routers/imagingStudies.router";
import PractitionersRouter from "./api/routers/practitioners.router";

const apiVersion = 1;
const apiPrefix = `/api/v${apiVersion}`;

const routes = (app: Application): void => {
  app.use(`${apiPrefix}/practitioners`, PractitionersRouter);
  app.use(`${apiPrefix}/patients`, PatientsRouter);
  app.use(`${apiPrefix}/holograms`, HologramsRouter);
  app.use(`${apiPrefix}/pipelines`, PipelinesRouter);
  app.use(`${apiPrefix}/imagingStudies`, ImagingStudiesRouter);
};

export default routes;
