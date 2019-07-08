import React, { Component } from "react";
import "./App.scss";
import MainContainer from "./MainContainer";
import { initializeIcons } from "@uifabric/icons";

// Note: See https://developer.microsoft.com/en-us/fabric/#/styles/web/icons#fabric-react
initializeIcons();

class App extends Component {
  render() {
    return (
      <div className="App">
        <MainContainer />
      </div>
    );
  }
}

export default App;
