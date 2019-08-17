import axios from "axios";

const { REACT_APP_BACKEND_HOST: host, REACT_APP_BACKEND_PORT: port, NODE_ENV } = process.env;
const timeout = parseInt(process.env.REACT_APP_BACKEND_TIMEOUT!);
const apiVersion = 1;
const apiPrefix = `/api/v${apiVersion}`;
const baseURL = `${host}:${port}${apiPrefix}`;

export const routes = {
  practitioners: "practitioners",
  patients: "patients",
  holograms: "holograms",
  pipelines: "pipelines",
  imagingStudies: "imagingStudies"
};

const headers = {
  Accept: "application/json"
};

const BackendServerAxios = axios.create({
  baseURL,
  timeout,
  headers
});

if (NODE_ENV !== "production") {
  console.info(`Connecting to backend at ${baseURL}`);
}

export default BackendServerAxios;
