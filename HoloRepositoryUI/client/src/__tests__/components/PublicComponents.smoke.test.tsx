import React from "react";
import { shallow } from "enzyme";
import AboutPage from "../../components/public/AboutPage";
import PublicContainer from "../../components/public/PublicContainer";
import LoginPage from "../../components/public/LoginPage";
import ErrorPage from "../../components/public/ErrorPage";

it("renders PublicContainer without crashing", () => {
  shallow(<PublicContainer />);
});

it("renders LandingPage without crashing", () => {
  shallow(<LoginPage />);
});

it("renders ErrorPage without crashing", () => {
  shallow(<ErrorPage />);
});

it("renders AboutPage without crashing", () => {
  shallow(<AboutPage />);
});
