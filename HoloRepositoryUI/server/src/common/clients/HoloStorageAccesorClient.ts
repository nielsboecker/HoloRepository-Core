const accessorBaseUrl = "http://localhost";
const port = 8080;
const apiPrefix = `api/1.0.0`;
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
  return `${baseURL}?pid=${pids}`;
};

export default {
  getBaseURL,
  getDownloadURL,
  getEndpointURL,
  getAllForPatientsURL
};
