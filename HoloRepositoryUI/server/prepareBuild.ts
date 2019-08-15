import { rm, mkdir, cp, test } from "shelljs";
import tsConfig from "./tsconfig.json";

// Create build target directory
const outDir = tsConfig.compilerOptions.outDir;
rm("-rf", outDir);
mkdir(outDir);

// Copy .env file
if (test("-e", ".env")) {
  cp(".env", `${outDir}/.env`);
}

// The rest of the build process will be handled by tsc
