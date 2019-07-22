import shelljs from 'shelljs';

const config = require('./tsconfig.json');
const outDir = config.compilerOptions.outDir;

// Create build target directory
shelljs.rm('-rf', outDir);
shelljs.mkdir(outDir);

// Copy .env file
shelljs.cp('.env', `${outDir}/.env`);

// The rest of the build process will be handled by tsc
