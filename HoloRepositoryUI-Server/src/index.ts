import "./common/env";
import Server from "./common/server";
import routes from "./routes";
import { getImagingStudySeries, getPatient, getPractitioner } from "./common/clients/fhirClient";

const port = parseInt(process.env.PORT);
const server = new Server().router(routes).listen(port);

const pid = "e13d1464-d401-4be4-8b90-e8edadd6dce1";
const patient = getPatient(pid);
patient.then(p => console.log(p));

const practitioner = getPractitioner("504b6374-d963-44ea-a733-1eaf31901e63");
practitioner.then(p => console.log(p));

const iss = getImagingStudySeries("5c889b73-46cc-41af-86b4-5cebfdc3637c")
  .then(i => console.log(i));

export default server;
