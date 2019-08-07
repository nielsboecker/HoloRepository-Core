import shelljs from "shelljs";
import tsConfig from "./tsconfig.json";

// Create build target directory
const outDir = tsConfig.compilerOptions.outDir;
shelljs.rm('-rf', outDir);
shelljs.mkdir(outDir);

// Copy .env file
shelljs.cp('.env', `${outDir}/.env`);

// The rest of the build process will be handled by tsc
