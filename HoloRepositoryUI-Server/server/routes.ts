import { Application } from 'express';
import examplesRouter from './api/controllers/examples/router'

const routes = (app: Application): void => {
  app.use('/api/v1/examples', examplesRouter);
};

export default routes;