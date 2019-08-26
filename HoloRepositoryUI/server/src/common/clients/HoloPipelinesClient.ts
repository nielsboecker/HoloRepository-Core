const { HOLOPIPELINES_HOST, HOLOPIPELINES_PORT } = process.env;
const apiPrefix = `api/v1`;
const baseURL = `${HOLOPIPELINES_HOST}:${HOLOPIPELINES_PORT}/${apiPrefix}`;

const getJobsURL = (): string => {
  return `${baseURL}/jobs`;
};

const getJobStatusURL = (jid: string): string => {
  return `${baseURL}/${jid}/state`;
};

const getJobLogURL = (jid: string): string => {
  return `${baseURL}/${jid}/log`;
};

const getPipelinesURL = (): string => {
  return `${baseURL}/pipelines`;
};

export default {
  getJobsURL,
  getJobStateURL: getJobStatusURL,
  getPipelinesURL
};
