# HoloRepositoryUI-Server <a href="https://dev.azure.com/MSGOSHHOLO/HoloRepository/_build/latest?definitionId=1&branchName=dev"><img src="https://dev.azure.com/MSGOSHHOLO/HoloRepository/_apis/build/status/HoloRepository-Core?branchName=dev&jobName=HoloRepositoryUI%20-%20Server" alt="Server build status" align="right" /></a>

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
```

### Environment variables

The app requires some environment variables to be set **at run-time**. You can refer to the `.env.local` file for guidance and either set them manually for local development, or copy the contents to a file called `.env`. The default values are taylored to a local dev environment, meaning all services are expected to run on `localhost`.

When building the program with `npm run compile`, the `.env` file will be copied to the `dist` folder, if it exists. I.e. any variables set in there will then be available at run-time. Alternatively, the variables can be set in the run-time environment manually.

### Docker example

```shell
docker build -t holorepository-ui-server -f ./server/Dockerfile .
docker run -d -p 3000:3001 --name holorepository-ui-server --env-file ./server/.env holorepository-ui-server:latest
```

Note that the `Dockerfile` is specified independently of the build context through the `-f` flag. This is necessary in order to copy `../types`, which would otherwise cause an error as it is outside the default build context. The build context needs to be the parent directory rather than this one.
