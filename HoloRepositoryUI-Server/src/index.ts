import "./common/env";
import Server from "./common/server";
import routes from "./routes";
import { getPatient } from "./services/clients/fhirClient";

const port = parseInt(process.env.PORT);
const server = new Server().router(routes).listen(port);

const patient = getPatient();
patient.then(p => console.log(p.name));

export default server;
