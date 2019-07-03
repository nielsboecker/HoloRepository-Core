import React, { Component } from "react";
import { RouteComponentProps } from "@reach/router";
import HologramsDetailsList from "./HologramsDetailsList";
import ContentContainer from "../core/ContentContainer";

class HologramsListPage extends Component<RouteComponentProps> {
  render() {
    return (
      <ContentContainer
        title="Your holograms"
        description={[
          `On this page, you will find a list of all holograms available for your patients. Click on a 
          hologram to inspect it and see a 3D preview.`,
          `Any new holograms you create will show up here, once they are generated.`
        ]}
      >
        <HologramsDetailsList />
      </ContentContainer>
    );
  }
}

export default HologramsListPage;
