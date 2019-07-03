import React, { Component } from "react";
import { RouteComponentProps } from "@reach/router";
import sampleHolograms from "../../__tests__/samples/sampleHolograms.json";
import { Hologram } from "../../types/index.jsx";

class HologramListPage extends Component<RouteComponentProps> {
  holograms = sampleHolograms as Hologram[];

  render() {
    return (
      <div>
        {this.holograms.map(hologram => (
          <div>
            <h1>{hologram.title}</h1>
          </div>
        ))}
      </div>
    );
  }
}

export default HologramListPage;
