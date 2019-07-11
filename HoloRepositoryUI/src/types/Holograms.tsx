import { IHumanName } from "./Patients";

/**
 * Interface representing one image series in a DICOM imaging study.
 * Semantics is similar to the corresponding FHIR resource.
 */
export interface IImagingStudySeries {
  id: string;
  subject: {
    id: string;
    name?: IHumanName;
  };
  previewPictureUrl?: string;
  description?: string;
  bodySite?: string;
  encounterDate?: string;
  modality?: string;
}

/**
 * Interface for a Hologram. Note that, similar to FHIR's ImagingStudy, the actual
 * binary data is not included, just an endpoint where it can be retrieved.
 */
export interface IHologram {
  id: string;
  endpoint: string;
  title: string;
  subject: {
    id: string;
    name?: IHumanName;
  };
  author: {
    id: string;
    name?: IHumanName;
  };
  createdDate: string;
  fileSizeInKb: number;
  imagingStudySeriesId?: string;
  description?: string;
  bodySite?: string;
  encounterDate?: string;
}

/**
 * Interface for a Pipeline in the HoloPipelines subsystem, corresponding to one
 * particular image processing flow.
 */
export interface IPipeline {
  id: string;
  name: string;
  description: string;
  inputConstraints: [string, string][];
  inputExampleImageUrl?: string;
  outputExampleImageUrl?: string;
}
