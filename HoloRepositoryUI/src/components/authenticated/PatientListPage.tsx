import React, { Component } from "react";
import { RouteComponentProps } from "@reach/router";
import { IPatient } from "../../types/index.jsx";
import samplePatients from "../../__tests__/samples/samplePatients.json";

class PatientListPage extends Component<RouteComponentProps> {
  patients = samplePatients as IPatient[];

  render() {
    return (
      <div>
        {this.patients.map(patient => (
          <div>
            <h1>{patient.name.first}</h1>
            <ul>
              <li>{patient.email ? patient.email : "No mail"}</li>
              <li>{patient.phone}</li>
            </ul>
          </div>
        ))}
      </div>
    );
  }
}

export default PatientListPage;
