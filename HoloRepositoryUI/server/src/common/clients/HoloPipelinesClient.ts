const { HOLOPIPELINES_HOST, HOLOPIPELINES_PORT } = process.env;
const apiPrefix = `api/v1`;
const baseURL = `${HOLOPIPELINES_HOST}:${HOLOPIPELINES_PORT}/${apiPrefix}`;

const getJobsURL = (): string => {
  return `${baseURL}/jobs`;
};

// TODO @Niels: Change to /state, and add /log
const getJobStatusURL = (jid: string): string => {
  return `${baseURL}/${jid}/status`;
};

const getPipelinesURL = (): string => {
  return `${baseURL}/pipelines`;
};

export default {
  getJobsURL,
  getJobStatusURL,
  getPipelinesURL
};
