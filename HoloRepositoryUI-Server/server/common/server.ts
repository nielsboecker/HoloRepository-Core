import express, { Application } from "express";
import path from "path";
import bodyParser from "body-parser";
import http from "http";
import os from "os";
import cookieParser from "cookie-parser";
import logger from "./logger";
import errorHandler from "../api/middlewares/error.handler";

const app = express();

export default class ExpressServer {
  public constructor() {
    // Set root app path
    const root = path.normalize(__dirname + "/../..");
    app.set("appPath", root + "client");

    // Set configuration
    app.use(bodyParser.json({ limit: process.env.REQUEST_LIMIT || "100kb" }));
    app.use(bodyParser.urlencoded({ extended: true, limit: process.env.REQUEST_LIMIT || "100kb" }));
    app.use(cookieParser(process.env.SESSION_SECRET));

    // Serve static assets
    app.use(express.static(`${root}/public`));
  }

  public router(routes: (app: Application) => void): ExpressServer {
    routes(app);
    app.use(errorHandler);
    return this;
  }

  public listen(port: string | number = process.env.PORT): Application {
    const welcome = port => () =>
      logger.info(
        `up and running in ${process.env.NODE_ENV ||
          "development"} @: ${os.hostname()} on port: ${port}}`
      );
    http.createServer(app).listen(port, welcome(port));
    return app;
  }
}
