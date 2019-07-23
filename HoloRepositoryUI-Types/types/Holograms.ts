import { IHumanName } from "./Patients";

/**
 * Interface representing one image series in a DICOM imaging study.
 * Semantics is similar to the corresponding FHIR resource.
 */
export interface IImagingStudySeries {
  issid: string;
  subject: {
    pid: string;
    name?: IHumanName;
  };
  endpoint: string;
  numberOfInstances: number;
  previewPictureUrl?: string;
  bodySite?: string;
  date?: string;
  modality?: string;
}

/**
 * Creation modes for holograms.
 */
export enum HologramCreationMode {
  generateFromImagingStudy = "GENERATE_FROM_IMAGING_STUDY",
  uploadExistingModel = "UPLOAD_EXISTING_MODEL"
}

/**
 * Interface for a Hologram. Note that, similar to FHIR's ImagingStudy, the actual
 * binary data is not included, just an endpoint where it can be retrieved.
 */
export interface IHologram {
  hid: string;
  title: string;
  subject: {
    pid: string;
    name?: IHumanName;
  };
  author: {
    aid: string;
    name?: IHumanName;
  };
  createdDate: string;
  fileSizeInKb: number;
  imagingStudySeriesId?: string;
  description?: string;
  bodySite?: string;
  encounterDate?: string;
  contentType?: string;
  pipelineId?: string;
  creationMode?: HologramCreationMode;
}

/**
 * Interface for a Pipeline in the HoloPipelines subsystem, corresponding to one
 * particular image processing flow.
 */
export interface IPipeline {
  plid: string;
  title: string;
  description: string;
  inputConstraints: [string, string][];
  inputExampleImageUrl?: string;
  outputExampleImageUrl?: string;
}
