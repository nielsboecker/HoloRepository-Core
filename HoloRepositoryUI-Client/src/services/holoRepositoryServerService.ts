import serverAxios, { routes } from "./holoRepositoryServerAxios";
import { IPatient, IPractitioner } from "../types/Patients";
import { IHologram, IImagingStudySeries, IPipeline } from "../types/Holograms";

export class HoloRepositoryServerService {
  public async getPractitioner(pid: string): Promise<IPractitioner | null> {
    return await serverAxios
      .get<IPractitioner>(`${routes.practitioners}/${pid}`)
      .then(practitioner => practitioner.data)
      .catch(error => {
        console.error(error);
        return null;
      });
  }

  public async getAllPatients(): Promise<IPatient[]> {
    return await serverAxios
      .get<IPatient[]>(routes.patients)
      .then(patients => patients.data)
      .catch(error => {
        console.error(error);
        return [];
      });
  }

  public async getHologramsForAllPatients(pids: string[]): Promise<IHologram[]> {
    return await serverAxios
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
    return await serverAxios
      .get<BinaryType>(`${routes.holograms}/${hid}/download`)
      .then(hologram => hologram.data)
      .catch(error => {
        console.error(error);
        return null;
      });
  }

  public async deleteHologramById(hid: string): Promise<boolean> {
    return await serverAxios
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

  public async getImagingStudySeriesForAllPatients(pids: string[]): Promise<IImagingStudySeries[]> {
    return await serverAxios
      .get<IImagingStudySeries[]>(`${routes.imagingStudySeries}`, {
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

  public async getImagingStudySeriesPreview(issid: string): Promise<string | unknown> {
    return await serverAxios
      .get<string>(`${routes.imagingStudySeries}/${issid}/preview`)
      .then(iss => iss.data)
      .catch(error => {
        console.error(error);
        return null;
      });
  }

  public async getAllPipelines(): Promise<IPipeline[]> {
    return await serverAxios
      .get<IPipeline[]>(routes.pipelines)
      .then(pipeline => pipeline.data)
      .catch(error => {
        console.error(error);
        return [];
      });
  }
}

export default new HoloRepositoryServerService();
