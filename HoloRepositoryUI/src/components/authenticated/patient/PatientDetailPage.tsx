import React, { Component } from "react";
import { RouteComponentProps } from "@reach/router";

interface IPatientDetailPageProps
  extends RouteComponentProps<{
    id: string;
  }> {}

class PatientDetailPage extends Component<IPatientDetailPageProps> {
  render() {
    return <div>PatientDetailPage for {this.props.id}</div>;
  }
}

export default PatientDetailPage;
