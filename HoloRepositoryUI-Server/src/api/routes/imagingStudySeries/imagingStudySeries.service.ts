import logger from "../../../common/logger";
import { IImagingStudySeries } from "../../../../../HoloRepositoryUI-Types";
import {
  getAllImagingStudySeries,
  getImagingStudySeries,
  getImagingStudySeriesForPatient
} from "../../../common/data.service";

// TODO: Endpoint, preview image

export class ImagingStudySeriesService {
  public getAll(): Promise<IImagingStudySeries[]> {
    logger.info("GET all ImagingStudySeries");
    return getAllImagingStudySeries();
  }

  public getAllForPatient(pid: string): Promise<IImagingStudySeries[]> {
    logger.info(`GET all ImagingStudySeries for 'Patient/${pid}'`);
    return getImagingStudySeriesForPatient(pid);
  }

  public getById(issid: string): Promise<IImagingStudySeries> {
    logger.info(`GET ImagingStudySeries by id '${issid}'`);
    return getImagingStudySeries(issid);
  }
}

export default new ImagingStudySeriesService();
