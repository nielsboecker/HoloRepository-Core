# HoloRepositoryUI-Client <a href="https://dev.azure.com/MSGOSHHOLO/HoloRepository/_build/latest?definitionId=1&branchName=dev"><img src="https://dev.azure.com/MSGOSHHOLO/HoloRepository/_apis/build/status/HoloRepository-Core?branchName=dev&jobName=HoloRepositoryUI%20-%20Client" alt="Client build status" align="right" /></a>

A web-based React application that allows practitioners to browse their patients and manage the generation of 3D models sourced from imaging studies like CT or MRI scans.

Please refer to `../README.md` for more information.

## Notes

- **TypeScript**: This app uses TypeScript to provide type safety, static analysis, code completion etc. If you get an error about types not being compiled, you have to `cd ../types` and `npm install & npm run build`.

## Deployment

### Environment variables

The app requires the following environment variables to be set **at build-time**:

- `REACT_APP_BACKEND_HOST`
- `REACT_APP_BACKEND_PORT`
- `REACT_APP_BACKEND_TIMEOUT`

When developing locally, React will default to the values in `.env.local`, which are taylored to a local dev environment, meaning all services are expected to run on `localhost`. This behaviour can be overridden by setting the variables manually or using a `.env.development.local` file (see [CRA docs](https://create-react-app.dev/docs/adding-custom-environment-variables) for more infos).

### Docker example

```shell
docker build \
    --build-arg REACT_APP_BACKEND_HOST=http://localhost \
    --build-arg REACT_APP_BACKEND_PORT=3001 \
    --build-arg REACT_APP_BACKEND_TIMEOUT=15000 \
    --tag holorepository-ui-client \
    --file ./client/Dockerfile .
docker run -d -p 3000:3000 --name holorepository-ui-client holorepository-ui-client:latest
```

Note that the `Dockerfile` is specified independently of the build context through the `-f` flag. This is necessary in order to copy `../types`, which would otherwise cause an error as it is outside the default build context. The build context needs to be the parent directory rather than this one.
