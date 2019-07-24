import { Application } from "express";
import PatientRouter from "./api/routes/patients/patient.router";
import HologramRouter from "./api/routes/hologram/hologram.router";
import PipelineRouter from "./api/routes/pipelines/pipeline.router";
import ImagingStudyRouter from "./api/routes/imagingStudy/imagingStudy.router";
import PractitionerRouter from "./api/routes/practitioner/practitioner.router";

const apiVersion = 1;
const apiPrefix = `/api/v${apiVersion}`;

const practitionerRoute = `${apiPrefix}/practitioner`;
const patientRoute = `${apiPrefix}/patient`;
const hologramRoute = `${apiPrefix}/hologram`;
const pipelineRoute = `${apiPrefix}/pipeline`;
const imagingStudyRoute = `${apiPrefix}/imagingStudy`;

const routes = (app: Application): void => {
  app.use(practitionerRoute, PractitionerRouter);
  app.use(patientRoute, PatientRouter);
  app.use(hologramRoute, HologramRouter);
  app.use(pipelineRoute, PipelineRouter);
  app.use(imagingStudyRoute, ImagingStudyRouter);
};

export default routes;
