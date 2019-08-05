import express, { Application } from "express";
import path from "path";
import bodyParser from "body-parser";
import http from "http";
import os from "os";
import logger from "./logger";
import cors from "cors";

const app = express();

export default class ExpressServer {
  public constructor() {
    // Set root app path
    const root = path.normalize(__dirname + "/../..");
    app.set("appPath", root + "client");

    // Set configuration
    app.use(bodyParser.json({ limit: process.env.REQUEST_LIMIT || "100kb" }));
    app.use(bodyParser.urlencoded({ extended: true, limit: process.env.REQUEST_LIMIT || "100kb" }));

    // Serve static assets
    app.use(express.static(`${root}/public`));
  }

  public router(routes: (app: Application) => void): ExpressServer {
    // Middleware before routes
    app.use(cors());

    routes(app);

    // Middleware after routes
    // Note: using default Express error handler for now, may change soon
    // app.use(errorHandler);

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
