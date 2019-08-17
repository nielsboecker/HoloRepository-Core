import React from "react";
import Formsy from "formsy-react";

/**
 * Wraps component with Formsy HOC. Needed for components that implement Formsy inputs
 * (for instance that access PassDownProps).
 */
export const wrapWithFormsy = (component: JSX.Element) => {
  return <Formsy>{component}</Formsy>;
};
