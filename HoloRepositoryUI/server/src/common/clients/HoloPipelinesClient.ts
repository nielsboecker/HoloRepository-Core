const { HOLOPIPELINES_HOST, HOLOPIPELINES_PORT } = process.env;
const apiPrefix = `api/v1`;
const baseURL = `${HOLOPIPELINES_HOST}:${HOLOPIPELINES_PORT}/${apiPrefix}`;
const jobsEndpoint = `${baseURL}/jobs`;
const pipelinesEndpoint = `${baseURL}/pipelines`;

const getJobsURL = (): string => {
  return jobsEndpoint;
};

const getJobStateURL = (jid: string): string => {
  return `${jobsEndpoint}/${jid}/state`;
};

const getJobLogURL = (jid: string): string => {
  return `${jobsEndpoint}/${jid}/log`;
};

const getPipelinesURL = (): string => {
  return pipelinesEndpoint;
};

export default {
  getJobsURL,
  getJobStateURL,
  getJobLogURL,
  getPipelinesURL
};
