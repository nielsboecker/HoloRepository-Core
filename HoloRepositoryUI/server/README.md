# HoloRepositoryUI-Server
Back-end for the HoloRepository UI that provides the front-end with a concise API, abstracting all interactions with other subsystems such as the hospital's FHIR server and PACS. Written in Express.js and Typescript.


## Development
```shell
# install dependencies
npm install

# run in development mode
npm run dev

# run in  debug mode
npm run dev:debug

# run tests
npm run test
```


### Local development
When run with `npm run dev`, the API server will be available at [http://localhost:3001/api/v1](http://localhost:3001/api/v1). It can be tested, for instance using `curl`:
```shell
curl http://localhost:3001/api/v1/patients
```

If you run the React client at the same time, it will be using port `3000` and accessing this back-end at `3001`.


### Notes
- **TypeScript**: This app uses TypeScript to provide type safety, static analysis, code completion etc. If you get an error about types not being compiled, you have to `cd ../types` and `npm install & npm run build`.


## Deployment


### Building the application locally
```shell
# compile and run in production mode
npm run compile && npm start
`````


### Building and running the docker image
```shell
docker build -t holorepository-ui-server -f ./Dockerfile ..

# run and map port to default HTTP port on the Docker host
docker run -p 80:3001 holorepository-ui-server:latest

# test connection
curl http://localhost/api/v1/patients
```

Note that the `Dockerfile` is specified independently of the build context through the `-f` flag. This is necessary in order to copy `../types`, which would otherwise cause an error as it is outside the default build context. The build context needs to be the parent directory rather than this one.
