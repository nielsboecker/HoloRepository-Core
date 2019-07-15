import { Router } from 'express';
import controller from './controller';

const ExamplesRouter = Router()
    .post('/', controller.create)
    .get('/', controller.all)
    .get('/:id', controller.byId);

export default ExamplesRouter;
