import React, { Component } from "react";
import { RouteComponentProps } from "@reach/router";
import Menu from "./Menu";

class AuthContainer extends Component<RouteComponentProps> {
  render() {
    return (
      <div>
        <Menu />
        AuthContainer
        {this.props.children}
      </div>
    );
  }
}

export default AuthContainer;
