import shelljs from 'shelljs';

const config = require('./tsconfig.json');
const outDir = config.compilerOptions.outDir;

shelljs.rm('-rf', outDir);
shelljs.mkdir(outDir);
shelljs.cp('.env', `${outDir}/.env`);
shelljs.mkdir('-p', `${outDir}/common/swagger`);
shelljs.cp('server/common/api.yml', `${outDir}/common/api.yml`);
