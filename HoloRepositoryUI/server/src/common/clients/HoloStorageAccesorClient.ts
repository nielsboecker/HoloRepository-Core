const accessorBaseUrl = "http://localhost";
const port = 3200;
const apiPrefix = `api/v1`;
const hologramsEndpoint = "holograms";
const baseURL = `${accessorBaseUrl}:${port}/${apiPrefix}/${hologramsEndpoint}`;

const getBaseURL = () => baseURL;

const getDownloadURL = (hid: string): string => {
  return `${baseURL}/${hid}/download`;
};

const getEndpointURL = (hid: string): string => {
  return `${baseURL}/${hid}`;
};

const getAllForPatientsURL = (pids: string): string => {
  return `${baseURL}?pids=${pids}`;
};

export default {
  getBaseURL,
  getDownloadURL,
  getEndpointURL,
  getAllForPatientsURL
};
