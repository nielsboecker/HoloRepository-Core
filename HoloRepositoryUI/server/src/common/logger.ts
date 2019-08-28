import pino from "pino";

const { APP_ID, LOG_LEVEL } = process.env;

const logger = pino({
  // Note: Default values needed as this runs before any test setup,
  // and will run as dependency of other components
  name: APP_ID || "holorepository-ui-server",
  level: LOG_LEVEL || "debug"
});

export default logger;
