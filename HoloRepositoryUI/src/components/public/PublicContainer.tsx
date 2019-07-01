import React, { Component } from "react";
import { RouteComponentProps } from "@reach/router";

class PublicContainer extends Component<RouteComponentProps> {
  render() {
    return (
      <div>
        PublicContainer
        {this.props.children}
      </div>
    );
  }
}

export default PublicContainer;
