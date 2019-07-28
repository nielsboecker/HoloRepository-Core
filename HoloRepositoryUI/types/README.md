# HoloRepository UI Types

This directory contains the TypeScript definitions that are used by multiple other sub-projects. Using project references and leveraging the mono-repository style of this project, the other sub-directories directly access the compiled definitions from this directory.

## Installation
For support of referenced projects, TypeScript >= 3.0 is required. To install it as an npm dev dependency, run `npm install`, followed by `npm run build` to compile.

## Development
For types kept directly in the React app, `noEmit` is set to `true`. However, to reference the definitions in this sub-directory, they have to be built, otherwise the TypeScript compiler in the referencing projects will throw an error. Therefore, evoking `npm run build` is necessary.

As the `dist` folder is ignored by VCS, any changes in `.ts` files require a recompile; otherwise, new changes will be ignored and the last compiled version will be referenced.

## Further reading
https://www.typescriptlang.org/docs/handbook/project-references.html