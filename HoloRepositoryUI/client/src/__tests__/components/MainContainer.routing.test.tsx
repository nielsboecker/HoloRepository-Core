import React from "react";
import { ReactWrapper } from "enzyme";
import MainContainer from "../../components/shared/MainContainer";
import AppContainer from "../../components/app/core/AppContainer";
import PublicContainer from "../../components/public/PublicContainer";
import { createHistory, createMemorySource, LocationProvider } from "@reach/router";
import LandingPage from "../../components/public/LandingPage";
import PatientListPage from "../../components/app/patients/PatientListPage";
import ErrorPage from "../../components/public/ErrorPage";
import { mountWithContextProvider } from "../../__test_utils__/MockContextProvider";

it("should render PublicContainer for route '/'", () => {
  const underTest = prepareAndMountComponent("/");
  expect(underTest.find(PublicContainer)).toHaveLength(1);
  expect(underTest.find(AppContainer)).toHaveLength(0);
});

it("should render LandingPage for route '/start'", () => {
  const underTest = prepareAndMountComponent("/start");
  expect(underTest.find(PublicContainer)).toHaveLength(1);
  expect(underTest.find(LandingPage)).toHaveLength(1);
});

it("should render LandingPage for invalid URLs outside the '/app' main route", () => {
  const underTest = prepareAndMountComponent("/foobar");
  expect(underTest.find(PublicContainer)).toHaveLength(1);
  expect(underTest.find(LandingPage)).toHaveLength(1);
});

it("should render AppContainer for route '/app'", () => {
  const underTest = prepareAndMountComponent("/app");
  expect(underTest.find(AppContainer)).toHaveLength(1);
  expect(underTest.find(PublicContainer)).toHaveLength(0);
});

it("should render PatientListPage for route '/app/patients'", () => {
  const underTest = prepareAndMountComponent("/app/patients");
  expect(underTest.find(AppContainer)).toHaveLength(1);
  expect(underTest.find(PatientListPage)).toHaveLength(1);
});

it("should render ErrorPage for invalid URLs under the '/app' main route", () => {
  const underTest = prepareAndMountComponent("/app/foobar");
  expect(underTest.find(AppContainer)).toHaveLength(1);
  expect(underTest.find(ErrorPage)).toHaveLength(1);
});

/**
 * Helper function to wrap a component in LocationProvider and mount it.
 */
function prepareAndMountComponent(route: string): ReactWrapper {
  return mountWithContextProvider(
    <LocationProvider history={createHistory(createMemorySource(route))}>
      <MainContainer />
    </LocationProvider>
  );
}
