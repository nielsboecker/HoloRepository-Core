import React from "react";
import PatientCard from "../../components/app/patients/PatientCard";

import samplePatients from "../samples/samplePatients.json";
import { getAgeFromDobString } from "../../util/PatientUtil";
import { IPatient } from "../../../../types";
import { mountWithContextProvider } from "../../__test_utils__/MockContextProvider";

it("should render patient details correctly", () => {
  const patient = samplePatients[0] as IPatient;
  const underTest = mountWithContextProvider(<PatientCard patient={patient} />);

  expect(underTest.find("h3").text()).toEqual("Beverly Cole");
  expect(underTest.find(".age").text()).toContain(`Age: ${getAgeFromDobString("1989-07-07")}`);
  expect(underTest.find(".gender").text()).toEqual("Gender: Female");
  expect(underTest.find(".numberOfHolograms").text()).toEqual("No holograms available");
});
