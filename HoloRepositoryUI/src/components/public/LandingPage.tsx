import React, { Component } from "react";
import { RouteComponentProps, Link } from "@reach/router";

class LandingPage extends Component<RouteComponentProps> {
  render() {
    return (
      <div>
        <h1>HoloRepository</h1>
        <Link to="/app/patients">Login</Link>
      </div>
    );
  }
}

export default LandingPage;
