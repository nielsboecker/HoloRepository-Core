import BackendServerAxios, { routes } from "./BackendServerAxios";
import {
  IHologram,
  IJobStateResponse,
  IHologramCreationRequest_Generate,
  IHologramCreationRequest_Upload,
  IImagingStudy,
  IPatient,
  IPipeline,
  IPractitioner
} from "../../../types";
import { PidToPatientsMap } from "../components/shared/AppState";
import { AxiosResponse } from "axios";

const handleError = (error: Error): any => {
  console.log("Encountered an error while fetching data from backend: ", error.message);
  return null;
};

export type HologramsCombinedResult = Record<string, IHologram[]>;
export type ImagingStudiesCombinedResult = Record<string, IImagingStudy[]>;

export class BackendServerService {
  public async getPractitioner(pid: string): Promise<IPractitioner | null> {
    return BackendServerAxios.get<IPractitioner>(`${routes.practitioners}/${pid}`)
      .then(practitioner => practitioner.data as IPractitioner)
      .catch(handleError);
  }

  public async getAllPatientsForPractitioner(pid: string): Promise<IPatient[] | null> {
    return BackendServerAxios.get<IPatient[]>(routes.patients, {
      params: {
        practitioner: pid
      }
    })
      .then(patients => patients.data as IPatient[])
      .catch(handleError);
  }

  public async getHologramsForAllPatients(
    patients: PidToPatientsMap
  ): Promise<HologramsCombinedResult | null> {
    return BackendServerAxios.get<HologramsCombinedResult>(`${routes.holograms}`, {
      params: {
        pids: _extractCombinedPidsString(patients)
      }
    })
      .then(holograms => holograms.data as HologramsCombinedResult)
      .catch(handleError);
  }

  public async downloadHologramById(hid: string): Promise<boolean | null> {
    return BackendServerAxios.get<BinaryType>(`${routes.holograms}/${hid}/download`, {
      responseType: "blob",
      headers: {
        Accept: "gltf-binary"
      }
    })
      .then(file => _forceDownload(file, `${hid}.glb`))
      .catch(handleError);
  }

  public async deleteHologramById(hid: string): Promise<boolean | null> {
    return BackendServerAxios.delete(`${routes.holograms}/${hid}`)
      .then(response => response.status === 200 || response.status === 204)
      .catch(handleError);
  }

  public async uploadHologram(
    metaData: IHologramCreationRequest_Upload
  ): Promise<IHologram | null> {
    const formData = new FormData();
    for (let [key, value] of Object.entries(metaData)) {
      // Note: Manually serialise objects, but not "hologramFile"
      if (key === "author" || key === "patient") {
        value = JSON.stringify(value);
      }
      formData.set(key, value);
    }

    return BackendServerAxios.post<IHologram>(`${routes.holograms}/upload`, formData, {
      headers: { "content-type": "multipart/form-data" }
    })
      .then(response => {
        if (response.status === 200 || response.status === 201) {
          return response.data;
        } else {
          return handleError(new Error(`Got response code ${response.status}`));
        }
      })
      .catch(handleError);
  }

  public async generateHologram(requestData: IHologramCreationRequest_Generate): Promise<string> {
    return BackendServerAxios.post(`${routes.pipelines}/generate`, requestData)
      .then(response => {
        if (response.status !== 202 || !response.data.jid) {
          throw new Error(
            `Got invalid response ${response.status}: ${JSON.stringify(response.data)}`
          );
        }
        return response.data.jid;
      })
      .catch(handleError);
  }

  public async getImagingStudiesForAllPatients(
    patients: PidToPatientsMap
  ): Promise<ImagingStudiesCombinedResult | null> {
    return BackendServerAxios.get<ImagingStudiesCombinedResult>(`${routes.imagingStudies}`, {
      params: { pids: _extractCombinedPidsString(patients) }
    })
      .then(iss => iss.data as ImagingStudiesCombinedResult)
      .catch(handleError);
  }

  public async getAllPipelines(): Promise<IPipeline[] | null> {
    return BackendServerAxios.get<Record<string, IPipeline>>(routes.pipelines)
      .then(pipeline => pipeline.data as Record<string, IPipeline>)
      .then(pipelineDict => Object.values(pipelineDict))
      .catch(handleError);
  }

  public async getJobStateById(jid: string): Promise<IJobStateResponse | null> {
    return BackendServerAxios.get<string>(`${routes.pipelines}/${jid}/state`)
      .then(response => response.data as IJobStateResponse)
      .catch(handleError);
  }

  public async getJobLogById(jid: string): Promise<string | null> {
    return BackendServerAxios.get<string>(`${routes.pipelines}/${jid}/log`)
      .then(response => response.data as string)
      .catch(handleError);
  }
}

const _extractCombinedPidsString = (patients: PidToPatientsMap): string => {
  return Object.keys(patients).join(",");
};

// Note: see https://gist.github.com/javilobo8/097c30a233786be52070986d8cdb1743
const _forceDownload = (response: AxiosResponse, fileName: string = "hologram.glb") => {
  const url = window.URL.createObjectURL(new Blob([response.data]));
  const link = document.createElement("a");
  link.href = url;
  link.setAttribute("download", fileName);
  document.body.appendChild(link);
  link.click();
  return true;
};

export default new BackendServerService();
