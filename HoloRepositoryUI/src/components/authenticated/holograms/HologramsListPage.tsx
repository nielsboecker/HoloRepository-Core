import React, { Component } from "react";
import { RouteComponentProps } from "@reach/router";
import { Hologram } from "../../../types/index.jsx";
import HologramsDetailsList from "./HologramsDetailsList";

class HologramsListPage extends Component<RouteComponentProps> {
  render() {
    return (
      <div>
        <h1>My holograms</h1>
        <HologramsDetailsList />
      </div>
    );
  }
}

export default HologramsListPage;
