/**
 * This snippet is automatically run before each test when invoking "yarn test".
 */
import { configure } from "enzyme";
import Adapter from "enzyme-adapter-react-16";
import { initializeIcons } from "@uifabric/icons";
import holoRepositoryServerAxios from "./services/holoRepositoryServerAxios";
import MockAdapter from "axios-mock-adapter";

// Configure Enzyme adaptedr
configure({ adapter: new Adapter() });

// Configure Axios mock adapter to prevent all actual network calls and just return 200 for now
const mock = new MockAdapter(holoRepositoryServerAxios);
mock.onAny().reply(200);

// Note: See https://developer.microsoft.com/en-us/fabric/#/styles/web/icons#fabric-react
initializeIcons();

// Note: See https://facebook.github.io/create-react-app/docs/running-tests
export default undefined;
