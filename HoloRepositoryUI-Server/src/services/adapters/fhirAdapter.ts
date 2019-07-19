import { IPatient } from "../../../../HoloRepositoryUI-Types";

const mapPatient = (patient: any): IPatient | null => {
  console.log("adapter");
  if (false) {
    return null;
  } else {
    return {
      birthDate: patient.birthDate,
      gender: patient.gender,
      name: patient.name[0].family,
      pid: patient.id
    };
  }
};

enum FhirResource {
  Patient,
  Practitioner
}

const getAdapter = (resource: FhirResource): Function => {
  switch (resource) {
    case FhirResource.Patient:
    default:
      return mapPatient;
  }
};

export { getAdapter, FhirResource };
