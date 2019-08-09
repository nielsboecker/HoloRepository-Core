import "./common/env";
import Server from "./common/server";
import routes from "./routes";

const port = parseInt(process.env.PORT) || 3001;
const server = new Server().router(routes).listen(port);

export default server;
