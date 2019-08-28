import express, { Application } from "express";
import path from "path";
import bodyParser from "body-parser";
import http from "http";
import os from "os";
import logger from "./logger";
import cors from "cors";

const app = express();

const { NODE_ENV, PORT, REQUEST_LIMIT } = process.env;
const rootPath = path.normalize(__dirname + "/../..");
const staticFilesPath = `${rootPath}/public`;

export default class ExpressServer {
  public constructor() {
    // Set root app path
    app.set("appPath", rootPath);

    // Set configuration
    app.use(bodyParser.json({ limit: REQUEST_LIMIT }));
    app.use(bodyParser.urlencoded({ extended: true, limit: REQUEST_LIMIT }));

    // Serve static assets
    app.use(express.static(staticFilesPath));
  }

  public router(routes: (app: Application) => void): ExpressServer {
    // Middleware before routes
    app.use(cors());

    routes(app);

    // Middleware after routes
    // Note: using default Express error handler for now
    // app.use(errorHandler);

    return this;
  }

  public listen(): Application {
    const welcomeMessage = () =>
      logger.info(`Up and running in ${NODE_ENV} @: ${os.hostname()} on port: ${PORT}}`);
    http.createServer(app).listen(PORT, welcomeMessage);
    return app;
  }
}
