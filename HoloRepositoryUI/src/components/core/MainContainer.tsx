import React, { Component } from "react";
import { Router } from "@reach/router";
import AuthContainer from "../authenticated/core/AuthContainer";
import PublicContainer from "../public/PublicContainer";
import AboutPage from "../public/AboutPage";
import LandingPage from "../public/LandingPage";
import ErrorPage from "../public/ErrorPage";
import DeviceConnectorPage from "../authenticated/DeviceConnectorPage";
import HologramListPage from "../authenticated/HologramListPage";
import PatientListPage from "../authenticated/PatientListPage";
import PatientDetailPage from "../authenticated/patient/PatientDetailPage";
import ProfileInformationPage from "../authenticated/ProfileInformationPage";

class MainContainer extends Component {
  render() {
    return (
      <>
        <p>MainContainer</p>

        <Router>
          <PublicContainer path="/">
            <LandingPage default path="start" />
            <AboutPage path="about" />
          </PublicContainer>

          <AuthContainer path="app">
            <PatientListPage path="patients" />
            <PatientDetailPage path="patient/:id" />
            <DeviceConnectorPage path="devices" />
            <HologramListPage path="holograms" />
            <ProfileInformationPage path="profile" />
            <ErrorPage default />
          </AuthContainer>
        </Router>
      </>
    );
  }
}

export default MainContainer;
