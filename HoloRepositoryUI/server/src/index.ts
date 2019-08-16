import "./common/env";
import Server from "./common/server";
import routes from "./routes";

const server = new Server().router(routes).listen();

export default server;
