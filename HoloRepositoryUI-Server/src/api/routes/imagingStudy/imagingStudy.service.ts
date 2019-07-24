import logger from "../../../common/logger";
import { IImagingStudy } from "../../../../../HoloRepositoryUI-Types";
import {
  getAllImagingStudies,
  getImagingStudy,
  getImagingStudiesForPatient
} from "../../../common/data.service";

export class ImagingStudyService {
  public getAll(): Promise<IImagingStudy[]> {
    logger.info("GET all ImagingStudies");
    return getAllImagingStudies();
  }

  public async getAllForPatient(pid: string): Promise<IImagingStudy[]> {
    logger.info(`GET all ImagingStudies for 'Patient/${pid}'`);
    return getImagingStudiesForPatient(pid);
  }

  public getById(isid: string): Promise<IImagingStudy> {
    logger.info(`GET ImagingStudies by id '${isid}'`);
    return getImagingStudy(isid);
  }
}

export default new ImagingStudyService();
