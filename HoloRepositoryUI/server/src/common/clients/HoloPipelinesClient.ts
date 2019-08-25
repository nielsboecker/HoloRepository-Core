const { HOLOPIPELINES_HOST, HOLOPIPELINES_PORT } = process.env;
const apiPrefix = `api/v1`;
const baseURL = `${HOLOPIPELINES_HOST}:${HOLOPIPELINES_PORT}/${apiPrefix}`;

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
