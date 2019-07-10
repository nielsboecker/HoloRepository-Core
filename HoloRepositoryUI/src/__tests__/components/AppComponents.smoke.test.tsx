import React from "react";
import { shallow } from "enzyme";
import AppContainer from "../../components/app/core/AppContainer";
import MenuHeader from "../../components/app/core/MenuHeader";

it("renders AppContainer without crashing", () => {
  shallow(<AppContainer />);
});

it("renders MenuHeader without crashing", () => {
  shallow(<MenuHeader />);
});

// TODO: Add tests for all, once design is stable
