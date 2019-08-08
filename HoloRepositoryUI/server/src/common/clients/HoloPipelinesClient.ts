const accessorBaseUrl = "http://localhost";
const port = 3100;
const apiPrefix = `api/v1`;
const baseURL = `${accessorBaseUrl}:${port}/${apiPrefix}`;

const getJobURL = (): string => {
  return `${baseURL}/job`;
};

const getJobStatusURL = (jid: string): string => {
  return `${baseURL}/${jid}/status`;
};

const getPipelinesURL = (): string => {
  return `${baseURL}/pipelines`;
};

export default {
  getJobURL,
  getJobStatusURL,
  getPipelinesURL
};
