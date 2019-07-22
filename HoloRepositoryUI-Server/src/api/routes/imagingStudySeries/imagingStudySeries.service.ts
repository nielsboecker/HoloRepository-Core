import logger from "../../../common/logger";
import { IImagingStudySeries } from "../../../../../HoloRepositoryUI-Types";
import { getImagingStudySeries } from "../../../common/data.service";

import sampleImagingStudySeries from "../../../__tests__/samples/internal/sampleImagingStudySeries.json";

const _sampleImagingStudySeries = sampleImagingStudySeries as IImagingStudySeries[];

export class ImagingStudySeriesService {
  public getAll(): Promise<IImagingStudySeries[]> {
    logger.info("GET all ImagingStudySeries");
    return Promise.resolve(_sampleImagingStudySeries);
  }

  public getById(issid: string): Promise<IImagingStudySeries> {
    logger.info(`GET ImagingStudySeries by id '${issid}'`);
    return getImagingStudySeries(issid);
  }

  public getPreviewById(issid: string): Promise<string> {
    // TODO: Implement
    logger.warn("ISS preview not implemented yet");

    const iss = _sampleImagingStudySeries.find(iss => iss.issid === issid);
    if (iss) {
      // TODO: Query PACS for image preview endpoint, return endpoint
      return Promise.resolve("<preview-url>");
    } else {
      return Promise.resolve(null);
    }
  }
}

export default new ImagingStudySeriesService();
