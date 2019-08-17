import express, { Application } from "express";
import path from "path";
import bodyParser from "body-parser";
import http from "http";
import os from "os";
import logger from "./logger";
import cors from "cors";

const app = express();

const { PORT: port, REQUEST_LIMIT: limit } = process.env;
const rootPath = path.normalize(__dirname + "/../..");
const staticFilesPath = `${rootPath}/public`;

export default class ExpressServer {
  public constructor() {
    // Set root app path
    app.set("appPath", rootPath);

    // Set configuration
    app.use(bodyParser.json({ limit }));
    app.use(bodyParser.urlencoded({ extended: true, limit }));

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
      logger.info(
        `Up and running in ${process.env.NODE_ENV} @: ${os.hostname()} on port: ${port}}`
      );
    http.createServer(app).listen(port, welcomeMessage);
    return app;
  }
}
