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

  expect(result.pid).toEqual("e13d1464-d401-4be4-8b90-e8edadd6dce1");
  expect(result.name).toEqual({
    full: "Cesar434 Macejkovic424",
    title: "Mr.",
    given: "Cesar434",
    family: "Macejkovic424"
  });
  expect(result.gender).toEqual("male");
  expect(result.birthDate).toEqual("1966-01-02T00:00:00.000Z");

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
