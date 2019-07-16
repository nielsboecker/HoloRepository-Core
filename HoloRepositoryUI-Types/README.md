# HoloRepository UI Types

This directory contains the TypeScript definitions that are used by multiple other sub-projects.

## Requirements
For support of referenced projects, TypeScript >= 3.0 is required.

## Development
For types kept directly in the React app, `noEmit` is set to `true`. However, to reference the definitions in this sub-directory, they have to be built, otherwise the TypeScript compiler in the referencing projects will throw an error. The command to compile the types is `tsc --build`.

As the `dist` folder is ignored by VCS, the types have to be compiled once initially. Note that any changes in `.ts` files require a recompile; otherwise, new changes will be ignored and the last compiled version will be referenced.

## Further reading
https://www.typescriptlang.org/docs/handbook/project-references.html