/**
 * Note: This project makes use of the rather recent TypeScript feature of
 * project references to bundle type definitions for different sub-projects
 * in a shared, separate directory. Unfortunately, restrictions of CRA only
 * allow to import interfaces from outside the src directory apparently.
 *
 * Therefore, enums  that are accessed programmatically are duplicated in
 * this file.
 *
 * Note that you may have to silence TypeScript errors with @ts-ignore if
 * you use the identical types from different directories.
 */

// Holograms.ts
export enum HologramCreationMode {
  GENERATE_FROM_IMAGING_STUDY = "GENERATE_FROM_IMAGING_STUDY",
  UPLOAD_EXISTING_MODEL = "UPLOAD_EXISTING_MODEL"
}
