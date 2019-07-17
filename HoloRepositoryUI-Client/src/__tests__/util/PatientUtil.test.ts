import {
  capitaliseString,
  getAgeFromDobString,
  getNumberOfHolograms
} from "../../util/PatientUtil";
// @ts-ignore TS7015
import mockNow from "jest-mock-now";
import sampleHolograms from "../samples/sampleHolograms.json";
import { IHologram } from "../../../../HoloRepositoryUI-Types";

it("capitaliseString capitalises a string correctly", () => {
  const input = "foo bar";
  const result = capitaliseString(input);
  expect(result).toEqual("Foo bar");
});

it("capitaliseString handles an already capitalisedstring correctly", () => {
  const input = "Foo bar";
  const result = capitaliseString(input);
  expect(result).toEqual("Foo bar");
});

it("getAgeFromDobString functions correctly", () => {
  mockNow(new Date("2014-01-01"));
  const input = "1989-07-07";
  const result = getAgeFromDobString(input);
  expect(result).toBe(24);
});

it("getNumberOfHolograms functions correctly", () => {
  const input = sampleHolograms as IHologram[];
  const result = getNumberOfHolograms(input);
  expect(result).toEqual("3 holograms available");
});

it("getNumberOfHolograms functions correctly for empty array", () => {
  const result = getNumberOfHolograms([]);
  expect(result).toEqual("No holograms available");
});
