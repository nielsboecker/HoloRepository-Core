const { HOLOSTORAGE_ACCESSOR_HOST, HOLOSTORAGE_ACCESSOR_PORT } = process.env;

const apiPrefix = `api/v1`;
const baseURL = `${HOLOSTORAGE_ACCESSOR_HOST}:${HOLOSTORAGE_ACCESSOR_PORT}/${apiPrefix}/holograms`;

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
