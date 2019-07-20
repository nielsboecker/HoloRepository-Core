import { R4 } from "@Ahryman40k/ts-fhir-types";
import { getAdapterFunction } from "../common/adapters/fhirAdapter";
import { SupportedFhirResourceType } from "../common/clients/fhirClient";
import { IPatient, IPractitioner } from "../../../HoloRepositoryUI-Types";

import samplePatient from "./samples/fhir/samplePatient.json";
import samplePractitioner from "./samples/fhir/samplePractitioner.json";

it("should map patients", () => {
  const input = samplePatient as R4.IPatient;
  const mapPatient = getAdapterFunction(SupportedFhirResourceType.Patient);
  const result: IPatient = mapPatient(input);

  expect(result.pid).toEqual("e13d1464-d401-4be4-8b90-e8edadd6dce1");
  expect(result.name).toEqual({
    full: "Cesar434 Macejkovic424",
    title: "Mr.",
    given: "Cesar434",
    family: "Macejkovic424"
  });
  expect(result.gender).toEqual("male");
  expect(result.birthDate).toEqual("1966-01-02");

  expect(result.pictureUrl).toBeUndefined();
});

it("should map practitioners", () => {
  const input = samplePractitioner as R4.IPractitioner;
  const mapPractitioner = getAdapterFunction(SupportedFhirResourceType.Practitioner);
  const result: IPractitioner = mapPractitioner(input);

  expect(result.pid).toEqual("e24af66a-20e9-405d-94b2-7ff9ae8cf9ad");
  expect(result.name).toEqual({
    full: "Andre610 Schneider199",
    title: "Dr.",
    given: "Andre610",
    family: "Schneider199"
  });
  expect(result.gender).toEqual("male");
});
