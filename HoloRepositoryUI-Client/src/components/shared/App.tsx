import React, { Component } from "react";
import "./App.scss";
import MainContainer from "./MainContainer";
import { initializeIcons } from "@uifabric/icons";
import BackendService from "../../services/holoRepositoryServerService";

// Note: See https://developer.microsoft.com/en-us/fabric/#/styles/web/icons#fabric-react
initializeIcons();

class App extends Component {
  componentDidMount(): void {
    // Note: Data fetching will be moved elsewhere once Redux is included
    const pidsWithHolograms = ["5d1bf4f164f57d1ff4656a8f", "5d1bf4f1d7429b38ce499c61"];
    const pidsWithIss = ["5d1bf4f1d32c1f6bf52331b9", "5d1bf4f17c56d264ea85264d"];

    BackendService.getPractitioner("foobar").then(p => console.log("practitioner", p));
    BackendService.getAllPatients().then(p => console.log("patients", p));
    BackendService.getHologramsForAllPatients(pidsWithHolograms).then(h =>
      console.log("holograms", h)
    );
    BackendService.getImagingStudySeriesForAllPatients(pidsWithIss).then(i =>
      console.log("iss", i)
    );
    BackendService.getAllPipelines().then(p => console.log("pipelines", p));
  }

  render() {
    return (
      <div className="App">
        <MainContainer />
      </div>
    );
  }
}

export default App;
