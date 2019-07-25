import serverAxios, { routes } from "./holoRepositoryServerAxios";
import {
  IPatient,
  IPractitioner,
  IHologram,
  IImagingStudy,
  IPipeline
} from "../../../HoloRepositoryUI-Types";
import { PidToPatientsMap } from "../components/shared/AppState";

const handleError = (error: Error): null => {
  console.log("Encountered an error while fetching data from backend: ", error.message);
  return null;
};

export type HologramsCombinedResult = Record<string, IHologram[]>;
export type ImagingStudiesCombinedResult = Record<string, IImagingStudy[]>;

export class HoloRepositoryServerService {
  public async getPractitioner(pid: string): Promise<IPractitioner | null> {
    return serverAxios
      .get<IPractitioner>(`${routes.practitioner}/${pid}`)
      .then(practitioner => practitioner.data)
      .catch(handleError);
  }

  public async getAllPatientsForPractitioner(pid: string): Promise<IPatient[] | null> {
    return serverAxios
      .get<IPatient[]>(routes.patient, {
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
      .get<HologramsCombinedResult>(`${routes.hologram}`, {
        params: {
          pids: _extractCombinedPidsString(patients)
        }
      })
      .then(holograms => holograms.data)
      .catch(handleError);
  }

  public async downloadHologramById(hid: string): Promise<BinaryType | null> {
    return serverAxios
      .get<BinaryType>(`${routes.hologram}/${hid}/download`)
      .then(hologram => hologram.data)
      .catch(handleError);
  }

  public async deleteHologramById(hid: string): Promise<boolean | null> {
    return serverAxios
      .delete(`${routes.hologram}/${hid}`)
      .then(() => true)
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
      .get<ImagingStudiesCombinedResult>(`${routes.imagingStudy}`, {
        params: { pids: _extractCombinedPidsString(patients) }
      })
      .then(iss => iss.data)
      .catch(handleError);
  }

  public async getImagingStudyPreview(isid: string): Promise<string | null> {
    return serverAxios
      .get<string>(`${routes.imagingStudy}/${isid}/preview`)
      .then(iss => iss.data)
      .catch(handleError);
  }

  public async getAllPipelines(): Promise<IPipeline[] | null> {
    return serverAxios
      .get<IPipeline[]>(routes.pipeline)
      .then(pipeline => pipeline.data)
      .catch(handleError);
  }
}

const _extractCombinedPidsString = (patients: PidToPatientsMap): string => {
  return Object.keys(patients).join(",");
};

export default new HoloRepositoryServerService();
