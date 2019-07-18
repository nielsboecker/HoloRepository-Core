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
