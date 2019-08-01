import React from "react";
import { mount } from "enzyme";
import { AppContext, IAppState, initialState } from "../components/shared/AppState";
import { IPractitioner } from "../../../types";

import samplePractitioner from "../__tests__/samples/samplePractitioner.json";

const defaultContext: IAppState = {
  ...initialState,
  practitioner: samplePractitioner as IPractitioner
};

/**
 * Wraps component with context in order to provide for components that rely on the Context API.
 */
export const mountWithContextProvider = (component: JSX.Element, context: IAppState = defaultContext) => {
  return mount(<AppContext.Provider value={context}>{component}</AppContext.Provider>);
};
