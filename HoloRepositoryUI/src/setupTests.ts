/**
 * This snippet is automatically run before each test when invoking "yarn test".
 */
import { configure } from "enzyme";
import Adapter from "enzyme-adapter-react-16";

configure({ adapter: new Adapter() });

export default undefined;
