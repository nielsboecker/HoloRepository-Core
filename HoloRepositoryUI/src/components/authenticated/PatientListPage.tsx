import React, { Component } from "react";
import { RouteComponentProps } from "@reach/router";
import { IPatient } from "../../types/index.jsx";
import samplePatients from "../../__tests__/samples/samplePatients.json";
import ContentContainer from "./core/ContentContainer";

class PatientListPage extends Component<RouteComponentProps> {
  patients = samplePatients as IPatient[];

  render() {
    return (
      <ContentContainer
        title="Your patients"
        description={[
          `On this page, you will find a list of your patients. Click on a patient to inspect their medical data and any holograms that are available for the them.`,
          `On the patient page, you can also create new holograms via file upload or triggering the HoloPipelines.`
        ]}
      >
        {this.patients.map(patient => (
          <div key={patient.id}>
            <h1>{patient.name.first}</h1>
            <ul>
              <li>{patient.email ? patient.email : "No mail"}</li>
              <li>{patient.phone}</li>
            </ul>
          </div>
        ))}
      </ContentContainer>
    );
  }
}

export default PatientListPage;
