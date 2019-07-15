import path from 'path';
import express, {Application} from 'express';
import { OpenApiValidator } from 'express-openapi-validator';
import errorHandler from '../api/middlewares/error.handler';

const installValidator = (app: Application, routes: (app: Application) => void) => {
    const apiSpecPath = path.join(__dirname, 'api.yml');
    app.use(process.env.OPENAPI_SPEC || '/spec', express.static(apiSpecPath));

    new OpenApiValidator({
        apiSpecPath,
    }).install(app);

    routes(app);
    app.use(errorHandler);
};

export default installValidator;