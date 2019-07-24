import axios from "axios";

const headers = {
  Accept: "application/json"
};

const apiVersion = 1;
const apiPrefix = `/api/v${apiVersion}`;

export const routes = {
  practitioner: "practitioner",
  patient: "patient",
  hologram: "hologram",
  pipeline: "pipeline",
  imagingStudy: "imagingStudy"
};

const holoRepositoryServerAxios = axios.create({
  baseURL: `http://localhost:3001${apiPrefix}`,
  // Note: High timeout value needed as app takes a long time to start in dev mode
  timeout: 4000,
  headers
});

export default holoRepositoryServerAxios;
