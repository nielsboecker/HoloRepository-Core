import serverAxios, { routes } from "./holoRepositoryServerAxios";
import {
  IPatient,
  IPractitioner,
  IHologram,
  IImagingStudy,
  IPipeline
} from "../../../types";
import { PidToPatientsMap } from "../components/shared/AppState";
import { AxiosResponse } from "axios";

const handleError = (error: Error): null => {
  console.log("Encountered an error while fetching data from backend: ", error.message);
  return null;
};

export type HologramsCombinedResult = Record<string, IHologram[]>;
export type ImagingStudiesCombinedResult = Record<string, IImagingStudy[]>;

export class HoloRepositoryServerService {
  public async getPractitioner(pid: string): Promise<IPractitioner | null> {
    return serverAxios
      .get<IPractitioner>(`${routes.practitioners}/${pid}`)
      .then(practitioner => practitioner.data)
      .catch(handleError);
  }

  public async getAllPatientsForPractitioner(pid: string): Promise<IPatient[] | null> {
    return serverAxios
      .get<IPatient[]>(routes.patients, {
        params: {
          practitioner: pid
        }
      })
      .then(patients => patients.data)
      .catch(handleError);
  }

  public async getHologramsForAllPatients(
    patients: PidToPatientsMap
  ): Promise<HologramsCombinedResult | null> {
    return serverAxios
      .get<HologramsCombinedResult>(`${routes.holograms}`, {
        params: {
          pids: _extractCombinedPidsString(patients)
        }
      })
      .then(holograms => holograms.data)
      .catch(handleError);
  }

  public async downloadHologramById(hid: string): Promise<boolean | null> {
    return serverAxios
      .get<BinaryType>(
        // Note: Mocked for now; change to `${routes.hologram}/${hid}/download`
        "https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/Duck/glTF-Binary/Duck.glb",
        {
          responseType: "blob",
          headers: {
            Accept: "gltf-binary"
          }
        }
      )
      .then(file => _forceDownload(file, `${hid}.glb`))
      .catch(handleError);
  }

  public async deleteHologramById(hid: string): Promise<boolean | null> {
    return serverAxios
      .delete(`${routes.holograms}/${hid}`)
      .then(response => response.status === 200 || response.status === 204)
      .catch(handleError);
  }

  public async uploadHologram(): Promise<boolean> {
    // TODO: Implement
    console.warn("Upload not implemented yet");
    return Promise.resolve(true);
  }

  public async generateHologram(): Promise<boolean | null> {
    // TODO: Implement
    console.warn("Generate not implemented yet");
    return Promise.resolve(true).catch(handleError);
  }

  public async getImagingStudiesForAllPatients(
    patients: PidToPatientsMap
  ): Promise<ImagingStudiesCombinedResult | null> {
    return serverAxios
      .get<ImagingStudiesCombinedResult>(`${routes.imagingStudies}`, {
        params: { pids: _extractCombinedPidsString(patients) }
      })
      .then(iss => iss.data)
      .catch(handleError);
  }

  public async getAllPipelines(): Promise<IPipeline[] | null> {
    return serverAxios
      .get<IPipeline[]>(routes.pipelines)
      .then(pipeline => pipeline.data)
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

export default new HoloRepositoryServerService();
