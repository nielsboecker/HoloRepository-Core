import axios from "axios";

const accessorBaseUrl = "http://localhost";
const port = 8080;
const apiPrefix = `api/1.0.0`;
const hologramsEndpoint = "holograms";
const baseURL = `${accessorBaseUrl}:${port}/${apiPrefix}/${hologramsEndpoint}`;

const _holoStorageAccessorAxios = axios.create({
  // Note: All data UI server stores/retrieves directly with Accessor is via holograms endpoint
  baseURL,
  // Note: High value due to super slow local development
  timeout: 30000
});

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

/**
 * @deprecated Use redirects instead
 */
const handleAxiosError = error => {
  if (error.response && error.response.data) {
    console.error(`Error ${error.response.data.errorCode}: "${error.response.data.errorMessage}"`);
  } else {
    console.error(error);
  }
  return null;
};

/**
 * @deprecated Use redirects instead
 */
const getJson = async <T = any>(url: string, params: Record<string, string> = {}): Promise<T> => {
  return _holoStorageAccessorAxios
    .get<T>(url, {
      params,
      headers: { Accept: "application/json" }
    })
    .then(response => response.data as T)
    .catch(handleAxiosError);
};

export default {
  getBaseURL,
  getDownloadURL,
  getEndpointURL,
  getAllForPatientsURL
};
