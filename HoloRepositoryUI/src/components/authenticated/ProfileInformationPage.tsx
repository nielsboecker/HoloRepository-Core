import React, { Component } from "react";
import { RouteComponentProps } from "@reach/router";
import samplePractitioner from "../../__tests__/samples/samplePractitioner.json";
import { Practitioner } from "../../types/index.jsx";

class ProfileInformationPage extends Component<RouteComponentProps> {
  practitioner = samplePractitioner as Practitioner;

  render() {
    return <div>{`Hello, ${this.practitioner.name.full}!`}</div>;
  }
}

export default ProfileInformationPage;
