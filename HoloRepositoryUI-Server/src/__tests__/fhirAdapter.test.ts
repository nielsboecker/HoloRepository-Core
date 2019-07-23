import { R4 } from "@Ahryman40k/ts-fhir-types";
import { _normaliseDateString, getAdapterFunction } from "../common/adapters/fhirAdapter";
import { SupportedFhirResourceType } from "../common/clients/fhirClient";
import { IPatient, IPractitioner, IImagingStudySeries } from "../../../HoloRepositoryUI-Types";

import samplePatient from "./samples/fhir/samplePatient.json";
import samplePractitioner from "./samples/fhir/samplePractitioner.json";
import sampleImagingStudy from "./samples/fhir/sampleImagingStudy.json";

it("should map patients", () => {
  const input = samplePatient as R4.IPatient;
  const mapPatient = getAdapterFunction(SupportedFhirResourceType.Patient);
  const result: IPatient = mapPatient(input);

  expect(result.pid).toEqual("fa8a04b6-a7dd-4b02-9975-faf8c6c36448");
  expect(result.name).toEqual({
    full: "Fermin Mills",
    title: "Mr.",
    given: "Fermin",
    family: "Mills"
  });
  expect(result.gender).toEqual("male");
  expect(result.birthDate).toEqual("1942-10-25T00:00:00.000Z");
  expect(result.phone).toEqual("555-115-8212");
  expect(result.address).toEqual({
    city: "Fall River",
    postcode: "02720",
    state: "Massachusetts",
    street: "1076 Dooley Burg Unit 4"
  });
  expect(result.pictureUrl).toEqual("https://randomuser.me/api/portraits/men/18.jpg");
});

it("should map practitioners", () => {
  const input = samplePractitioner as R4.IPractitioner;
  const mapPractitioner = getAdapterFunction(SupportedFhirResourceType.Practitioner);
  const result: IPractitioner = mapPractitioner(input);

  expect(result.pid).toEqual("c2675859-493c-47c4-a7e0-376689cc4d5c");
  expect(result.name).toEqual({
    full: "Stanford Leannon",
    title: "Dr.",
    given: "Stanford",
    family: "Leannon"
  });
  expect(result.gender).toEqual("male");
});

it("should map imaging studies", () => {
  const input = sampleImagingStudy as R4.IImagingStudy;
  const mapImagingStudySeries = getAdapterFunction(SupportedFhirResourceType.ImagingStudySeries);
  const result: IImagingStudySeries = mapImagingStudySeries(input);
  expect(result.issid).toEqual("5c889b73-46cc-41af-86b4-5cebfdc3637c");
  expect(result.bodySite).toEqual("Chest");
  expect(result.date).toEqual("2013-07-29T00:00:00.000Z");
  expect(result.modality).toEqual("Digital Radiography");
  expect(result.numberOfInstances).toBe(1);
  expect(result.subject).toBeDefined();
  expect(result.subject.pid).toEqual("e13d1464-d401-4be4-8b90-e8edadd6dce1");

  expect(result.subject.name).toBeUndefined();
  expect(result.previewPictureUrl).toBeUndefined();
});

it("should normalise dates correctly", () => {
  const input = "2013-07-29T18:13:10+01:00";
  const result = _normaliseDateString(input);
  expect(result).toEqual("2013-07-29T00:00:00.000Z");
});
