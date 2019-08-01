import { Request, Response } from "express";

// eslint-disable-next-line no-unused-vars, no-shadow
const errorHandler = (err, req: Request, res: Response) => {
  const errors = err.errors || [{ message: err.message }];
  res.status(err.status || 500).json({ errors });
};

export default errorHandler;
