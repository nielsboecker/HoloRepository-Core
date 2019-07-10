import React from "react";
import { shallow } from "enzyme";
import App from "../../components/shared/App";
import MainContainer from "../../components/shared/MainContainer";
import MainFooter from "../../components/shared/MainFooter";

it("renders App without crashing", () => {
  shallow(<App />);
});

it("renders MainContainer without crashing", () => {
  shallow(<MainContainer />);
});

it("renders MainFooter without crashing", () => {
  shallow(<MainFooter />);
});
