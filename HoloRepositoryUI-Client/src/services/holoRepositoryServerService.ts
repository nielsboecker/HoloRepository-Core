import serverAxios, { routes } from "./holoRepositoryServerAxios";
import {
  IPatient,
  IPractitioner,
  IHologram,
  IImagingStudy,
  IPipeline
} from "../../../../HoloRepository-Core/HoloRepositoryUI-Types";

export class HoloRepositoryServerService {
  public async getPractitioner(pid: string): Promise<IPractitioner | null> {
    return serverAxios
      .get<IPractitioner>(`${routes.practitioner}/${pid}`)
      .then(practitioner => practitioner.data)
      .catch(error => {
        console.error(error);
        return null;
      });
  }

  public async getAllPatients(): Promise<IPatient[]> {
    return serverAxios
      .get<IPatient[]>(routes.patient)
      .then(patients => patients.data)
      .catch(error => {
        console.error(error);
        return [];
      });
  }

  public async getHologramsForAllPatients(pids: string[]): Promise<IHologram[]> {
    return serverAxios
      .get<IHologram[]>(`${routes.holograms}`, {
        params: {
          pids: pids.join(",")
        }
      })
      .then(holograms => holograms.data)
      .catch(error => {
        console.error(error);
        return [];
      });
  }

  public async downloadHologramById(hid: string): Promise<BinaryType | null> {
    return serverAxios
      .get<BinaryType>(`${routes.holograms}/${hid}/download`)
      .then(hologram => hologram.data)
      .catch(error => {
        console.error(error);
        return null;
      });
  }

  public async deleteHologramById(hid: string): Promise<boolean> {
    return serverAxios
      .delete(`${routes.holograms}/${hid}`)
      .then(() => true)
      .catch(error => {
        console.error(error);
        return false;
      });
  }

  public async uploadHologram(): Promise<boolean> {
    // TODO: Implement
    console.warn("Upload not implemented yet");
    return Promise.resolve(true);
  }

  public async generateHologram(): Promise<boolean> {
    // TODO: Implement
    console.warn("Generate not implemented yet");
    return Promise.resolve(true);
  }

  public async getImagingStudiesForAllPatients(pids: string[]): Promise<IImagingStudy[]> {
    return serverAxios
      .get<IImagingStudy[]>(`${routes.imagingStudy}`, {
        params: {
          pids: pids.join(",")
        }
      })
      .then(iss => iss.data)
      .catch(error => {
        console.error(error);
        return [];
      });
  }

  public async getImagingStudyPreview(isid: string): Promise<string | unknown> {
    return serverAxios
      .get<string>(`${routes.imagingStudy}/${isid}/preview`)
      .then(iss => iss.data)
      .catch(error => {
        console.error(error);
        return null;
      });
  }

  public async getAllPipelines(): Promise<IPipeline[]> {
    return serverAxios
      .get<IPipeline[]>(routes.pipeline)
      .then(pipeline => pipeline.data)
      .catch(error => {
        console.error(error);
        return [];
      });
  }
}

export default new HoloRepositoryServerService();
