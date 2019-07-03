import React, { Component } from "react";
import { RouteComponentProps } from "@reach/router";
import samplePractitioner from "../../__tests__/samples/samplePractitioner.json";
import { IPractitioner } from "../../types/index.jsx";
import ContentContainer from "./core/ContentContainer";

class ProfileInformationPage extends Component<RouteComponentProps> {
  practitioner = samplePractitioner as IPractitioner;

  render() {
    return (
      <ContentContainer title="Your profile" description={[]}>
        <div>{`Hello, ${this.practitioner.name.full}!`}</div>
      </ContentContainer>
    );
  }
}

export default ProfileInformationPage;
