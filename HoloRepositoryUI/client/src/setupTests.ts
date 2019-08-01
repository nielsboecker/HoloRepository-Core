/**
 * This snippet is automatically run before each test when invoking "yarn test".
 */
import { configure } from "enzyme";
import Adapter from "enzyme-adapter-react-16";
import { initializeIcons } from "@uifabric/icons";

configure({ adapter: new Adapter() });

// Note: See https://developer.microsoft.com/en-us/fabric/#/styles/web/icons#fabric-react
initializeIcons();

// Note: See https://facebook.github.io/create-react-app/docs/running-tests
export default undefined;
