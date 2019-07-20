import samplePatient from "./samples/fhir/samplePatient.json"
import { R4 } from "@Ahryman40k/ts-fhir-types";
import { getAdapterFunction } from "../common/adapters/fhirAdapter";
import { SupportedFhirResourceType } from "../common/clients/fhirClient";
import { IPatient } from "../../../HoloRepositoryUI-Types"

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