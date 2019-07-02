import React from "react";
import { shallow } from "enzyme";
import AuthContainer from "../../components/authenticated/core/AuthContainer";
import MenuHeader from "../../components/authenticated/core/MenuHeader";

it("renders AuthContainer without crashing", () => {
  shallow(<AuthContainer />);
});

it("renders MenuHeader without crashing", () => {
  shallow(<MenuHeader />);
});

// TODO: Add tests for all, once design is stable
