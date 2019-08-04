# HoloRepositoryUI-Server <a href="https://dev.azure.com/MSGOSHHOLO/HoloRepository/_build/latest?definitionId=1&branchName=dev"><img src="https://dev.azure.com/MSGOSHHOLO/HoloRepository/_apis/build/status/HoloRepository-Core?branchName=dev&jobName=HoloRepositoryUI%20-%20Server" alt="Server build status" align="right" /></a>

Back-end for the HoloRepository UI that provides the front-end with a concise API, abstracting all interactions with other subsystems such as the hospital's FHIR server and PACS.

The back-end is written in Express.js and Typescript.

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

# compile and run in production mode
npm run compile && npm start
```

### Local development

When run with `npm run dev`, the API server will be available at [http://localhost:3001/api/v1](http://localhost:3001/api/v1). It can be tested, for instance using `curl`:

```shell
curl localhost:3001/api/v1/patients
```

If you run the React client at the same time, it will be using port `3000` and accessing this back-end at `3001`.

### Notes

- **TypeScript**: This app uses TypeScript to provide type safety, static analysis, code completion etc. If you get an error about types not being compiled, you have to `cd ../types` and `npm install & npm run build`.

---

## Deployment

> TODO
