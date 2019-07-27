/**
 * This snippet is automatically run before each test when invoking "yarn test".
 */
import { configure, mount } from "enzyme";
import Adapter from "enzyme-adapter-react-16";
import { initializeIcons } from "@uifabric/icons";
import { AppContext, IAppState, initialState } from "./components/shared/AppState";
import samplePractitioner from "./__tests__/samples/samplePractitioner.json";
import React from "react";
import { IPractitioner } from "../../HoloRepositoryUI-Types";

configure({ adapter: new Adapter() });

// Note: See https://developer.microsoft.com/en-us/fabric/#/styles/web/icons#fabric-react
initializeIcons();

const defaultContext: IAppState = {
  ...initialState,
  practitioner: samplePractitioner as IPractitioner
};

/**
 * Wraps component with context in order to provide for components that rely on the Context API.
 */
export const mountWithContextProvider = (component: JSX.Element, context: IAppState = defaultContext) => {
  mount(<AppContext.Provider value={context}>{component}</AppContext.Provider>);
};

// Note: See https://facebook.github.io/create-react-app/docs/running-tests
// export default undefined;
