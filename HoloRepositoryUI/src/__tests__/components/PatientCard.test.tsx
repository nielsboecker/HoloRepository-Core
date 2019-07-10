import React from "react";
import PatientCard from "../../components/app/patients/PatientCard";
import { shallow } from "enzyme";

import samplePatientsWithHolograms from "../samples/samplePatientsWithHolograms.json";
import { IPatient } from "../../types";

it("should render patient details correctly", () => {
  const patient = samplePatientsWithHolograms[0] as IPatient;
  const undertTest = shallow(<PatientCard patient={patient} />);

  expect(undertTest.find("h3").text()).toEqual("Lorraine Cline");
  expect(undertTest.find(".age").text()).toEqual("Age: 29");
  expect(undertTest.find(".gender").text()).toEqual("Gender: Female");
  expect(undertTest.find(".numberOfHolograms").text()).toEqual("2 holograms available.");
});
