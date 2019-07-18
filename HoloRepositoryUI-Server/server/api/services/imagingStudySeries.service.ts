import logger from "../../common/logger";
import { IImagingStudySeries } from "../../../../HoloRepositoryUI-Types";

import sampleImagingStudySeries from "../../../test/samples/sampleImagingStudySeries.json";

const _sampleImagingStudySeries = sampleImagingStudySeries as IImagingStudySeries[];

export class ImagingStudySeriesService {
  public getAll(): Promise<IImagingStudySeries[]> {
    logger.info("GET all ImagingStudySeries");
    return Promise.resolve(_sampleImagingStudySeries);
  }

  public getById(issid: string): Promise<IImagingStudySeries> {
    logger.info(`GET ImagingStudySeries by id '${issid}'`);
    const iss = _sampleImagingStudySeries.find(iss => iss.issid === issid);
    if (iss) {
      return Promise.resolve(iss);
    } else {
      return Promise.resolve(null);
    }
  }
}

export default new ImagingStudySeriesService();
