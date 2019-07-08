import React, { Component } from "react";
import { RouteComponentProps } from "@reach/router";
import ContentContainer from "../core/ContentContainer";
import PatientCardsList from "./PatientCardsList";

class PatientListPage extends Component<RouteComponentProps> {
  render() {
    return (
      <ContentContainer
        title="Your patients"
        description={[
          `On this page, you will find a list of your patients. Click on a patient to inspect their medical data and any holograms that are available for the them.`,
          `On the patient page, you can also create new holograms via file upload or triggering the HoloPipelines.`
        ]}
      >
        <PatientCardsList />
      </ContentContainer>
    );
  }
}

export default PatientListPage;
