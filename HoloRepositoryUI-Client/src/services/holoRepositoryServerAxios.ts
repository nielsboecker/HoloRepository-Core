import axios from "axios";

const headers = {
  Accept: "application/json"
};

const apiVersion = 1;
const apiPrefix = `/api/v${apiVersion}`;

export const routes = {
  practitioners: "practitioners",
  patients: "patients",
  holograms: "holograms",
  pipelines: "pipelines",
  imagingStudies: "imagingStudies"
};

const holoRepositoryServerAxios = axios.create({
  baseURL: `http://localhost:3001${apiPrefix}`,
  timeout: 2500,
  headers
});

export default holoRepositoryServerAxios;
