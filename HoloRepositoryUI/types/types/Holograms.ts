import { IHumanName } from "./Patients";

/**
 * Interface representing one image series in a DICOM imaging study. For this project, we assume that every study
 * just hosts exactly one series, so the concepts are used interchangeably.
 * Semantics is similar to the corresponding FHIR resource.
 */
export interface IImagingStudy {
  isid: string;
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
  GENERATE_FROM_IMAGING_STUDY = "GENERATE_FROM_IMAGING_STUDY",
  UPLOAD_EXISTING_MODEL = "UPLOAD_EXISTING_MODEL",
  FROM_DEPTHVISOR_RECORDING = "FROM_DEPTHVISOR_RECORDING"
}

/**
 * Interface for a Hologram. Note that, similar to FHIR's ImagingStudy, the actual
 * binary data is not included, just an endpoint where it can be retrieved.
 */
export interface IHologram {
  hid: string;
  title: string;
  pid: string;
  aid: string;
  fileSizeInKb: number;
  creationDate: string;
  creationDescription?: string;
  creationMode?: HologramCreationMode;
  description?: string;
  bodySite?: string;
  dateOfImaging?: string;
  contentType?: string;
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
