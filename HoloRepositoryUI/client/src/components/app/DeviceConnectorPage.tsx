import React, { Component } from "react";
import { RouteComponentProps } from "@reach/router";
import ContentContainer from "./core/ContentContainer";

class DeviceConnectorPage extends Component<RouteComponentProps> {
  render() {
    return (
      <ContentContainer
        title="Your devices"
        description={[
          `To inspect your holograms on a Microsoft HoloLens, download the HoloRepository 
          application on your device. You will be prompted to enter a 5-digit PIN to authenticate yourself. 
          Use the code on this page to link your HoloLens application with your SMART on FHIR login.`
        ]}
      >
        <div>This feature is not available yet.</div>
      </ContentContainer>
    );
  }
}

export default DeviceConnectorPage;
