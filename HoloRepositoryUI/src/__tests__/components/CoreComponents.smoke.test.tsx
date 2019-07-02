import React from "react";
import { shallow } from "enzyme";
import App from "../../components/core/App";
import MainContainer from "../../components/core/MainContainer";
import MainFooter from "../../components/core/MainFooter";

it("renders App without crashing", () => {
  shallow(<App />);
});

it("renders MainContainer without crashing", () => {
  shallow(<MainContainer />);
});

it("renders MainFooter without crashing", () => {
  shallow(<MainFooter />);
});
