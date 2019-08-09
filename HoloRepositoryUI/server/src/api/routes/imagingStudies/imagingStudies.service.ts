import logger from "../../../common/logger";
import { IImagingStudy } from "../../../../../types";
import FhirClient, { SupportedFhirResourceType } from "../../../common/clients/fhirClient";
import { R4 } from "@ahryman40k/ts-fhir-types";

export class ImagingStudiesService {
  public getAll(): Promise<IImagingStudy[]> {
    logger.info("GET all ImagingStudies");
    return FhirClient.getAllAndMap<R4.IImagingStudy, IImagingStudy>(
      SupportedFhirResourceType.ImagingStudy
    );
  }

  public async getAllForPatient(pid: string): Promise<IImagingStudy[]> {
    logger.info(`GET all ImagingStudies for 'Patient/${pid}'`);
    return FhirClient.getAllAndMap<R4.IImagingStudy, IImagingStudy>(
      SupportedFhirResourceType.ImagingStudy,
      { patient: pid }
    );
  }

  public getById(isid: string): Promise<IImagingStudy> {
    logger.info(`GET ImagingStudies by id '${isid}'`);
    return FhirClient.getAndMap<R4.IImagingStudy, IImagingStudy>(
      SupportedFhirResourceType.ImagingStudy,
      isid
    );
  }
}

export default new ImagingStudiesService();
