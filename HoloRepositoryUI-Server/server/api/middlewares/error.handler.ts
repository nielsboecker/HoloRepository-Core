import { NextFunction, Request, Response } from "express";

// eslint-disable-next-line no-unused-vars, no-shadow
const errorHandler = (err, req: Request, res: Response, next: NextFunction) => {
  const errors = err.errors || [{ message: err.message }];
  res.status(err.status || 500).json({ errors });
};

export default errorHandler;