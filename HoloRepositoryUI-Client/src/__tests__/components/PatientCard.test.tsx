import React from "react";
import PatientCard from "../../components/app/patients/PatientCard";
import { shallow } from "enzyme";

import samplePatientsWithHolograms from "../samples/samplePatientsWithHolograms.json";
import { getAgeFromDobString } from "../../util/PatientUtil";
import { IPatient } from "../../../../HoloRepositoryUI-Types";

it("should render patient details correctly", () => {
  const patient = samplePatientsWithHolograms[0] as IPatient;
  const underTest = shallow(<PatientCard patient={patient} />);

  expect(underTest.find("h3").text()).toEqual("Lorraine Cline");
  expect(underTest.find(".age").text()).toContain(`Age: ${getAgeFromDobString("1989-07-07")}`);
  expect(underTest.find(".gender").text()).toEqual("Gender: Female");
  expect(underTest.find(".numberOfHolograms").text()).toEqual("2 holograms available");
});
