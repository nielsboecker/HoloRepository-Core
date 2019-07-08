import React, { Component } from "react";
import { RouteComponentProps } from "@reach/router";

class PublicContainer extends Component<RouteComponentProps> {
  render() {
    return <div>{this.props.children}</div>;
  }
}

export default PublicContainer;
