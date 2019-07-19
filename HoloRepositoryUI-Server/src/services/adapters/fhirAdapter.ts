import { IPatient } from "../../../../HoloRepositoryUI-Types";
import { R4 } from  '@Ahryman40k/ts-fhir-types';

const mapPatient = (patient: R4.IPatient): IPatient | null => {
  console.log("adapter");
  if (false) {
    return null;
  } else {
    return {
      birthDate: patient.birthDate,
      gender: patient.gender,
      name: {
        full: patient.name[0].family,
      },
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
