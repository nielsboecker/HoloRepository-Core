import React, { Component } from "react";
import { RouteComponentProps } from "@reach/router";
import ContentContainer from "./core/ContentContainer";
import { PropsWithContext, withAppContext } from "../shared/AppState";

class HoloLensRemoteLoginPage extends Component<RouteComponentProps & PropsWithContext> {
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
        <div>
          Your authentication PIN: <b>{this.props.context!.pin}</b>
        </div>
      </ContentContainer>
    );
  }
}

export default withAppContext(HoloLensRemoteLoginPage);
