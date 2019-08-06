import axios from "axios";

const accessorBaseUrl = "http://localhost";
const port = 8080;
const apiPrefix = `api/1.0.0`;
const hologramsEndpoint = "holograms";

const _holoStorageAccessorAxios = axios.create({
  // Note: All data UI server stores/retrieves directly with Accessor is via holograms endpoint
  baseURL: `${accessorBaseUrl}:${port}/${apiPrefix}/${hologramsEndpoint}`,
  timeout: 4000
});

const handleAxiosError = error => {
  console.error(`Error ${error.response.data.errorCode}: "${error.response.data.errorMessage}"`);
  return null;
};

const get = async <T = any>(url: string, params: Record<string, string> = {}) => {
  return _holoStorageAccessorAxios
    .get<T>(url, { params })
    .then(response => response.data as T)
    .catch(handleAxiosError);
};

export default {
  get
};
