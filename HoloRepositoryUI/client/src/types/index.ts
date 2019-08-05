/**
 * Note: This project makes use of the rather recent TypeScript feature of
 * project references to bundle type definitions for different sub-projects
 * in a shared, separate directory. Unfortunately, restrictions of CRA only
 * allow to import interfaces from outside the src directory apparently.
 *
 * Therefore, enums  that are accessed programmatically are duplicated in
 * this file.
 */

// Holograms.ts
export enum HologramCreationMode {
  generateFromImagingStudy = "GENERATE_FROM_IMAGING_STUDY",
  uploadExistingModel = "UPLOAD_EXISTING_MODEL"
}
