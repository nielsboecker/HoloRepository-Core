import React from "react";
import Enzyme, { mount, ReactWrapper } from "enzyme";
import Adapter from "enzyme-adapter-react-16";
import MainContainer from "../../components/core/MainContainer";
import AuthContainer from "../../components/authenticated/core/AuthContainer";
import PublicContainer from "../../components/public/PublicContainer";
import {
  LocationProvider,
  createHistory,
  createMemorySource
} from "@reach/router";
import LandingPage from "../../components/public/LandingPage";
import PatientListPage from "../../components/authenticated/PatientListPage";
import ErrorPage from "../../components/public/ErrorPage";

Enzyme.configure({ adapter: new Adapter() });

it("should render PublicContainer for route '/'", () => {
  const underTest = prepareAndMountComponent("/");
  expect(underTest.find(PublicContainer)).toHaveLength(1);
  expect(underTest.find(AuthContainer)).toHaveLength(0);
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

it("should render AuthContainer for route '/app'", () => {
  const underTest = prepareAndMountComponent("/app");
  expect(underTest.find(AuthContainer)).toHaveLength(1);
  expect(underTest.find(PublicContainer)).toHaveLength(0);
});

it("should render PatientListPage for route '/app/patients'", () => {
  const underTest = prepareAndMountComponent("/app/patients");
  expect(underTest.find(AuthContainer)).toHaveLength(1);
  expect(underTest.find(PatientListPage)).toHaveLength(1);
});

it("should render ErrorPage for invalid URLs under the '/app' main route", () => {
  const underTest = prepareAndMountComponent("/app/foobar");
  expect(underTest.find(AuthContainer)).toHaveLength(1);
  expect(underTest.find(ErrorPage)).toHaveLength(1);
});

/**
 * Helper function to wrap a component in LocationProvider and mount it.
 */
function prepareAndMountComponent(route: string): ReactWrapper {
  return mount(
    <LocationProvider history={createHistory(createMemorySource(route))}>
      <MainContainer />
    </LocationProvider>
  );
}
