# HoloRepositoryUI-Client

A web-based React application that allows practitioners to browse their patients and manage the generation of 3D models sourced from imaging studies like CT or MRI scans.


## Notes
- **TypeScript**: This app uses TypeScript to provide type safety, static analysis, code completion etc. If you get an error about types not being compiled, you have to `cd ../types` and `npm install & npm run build`.


## Deployment


### Building the application locally
```shell
npm run build
`````


### Building and running the docker image
```shell
docker build -t holorepository-ui-client -f ./Dockerfile ..

# run and map port to default HTTP port on the Docker host
docker run -d -p 80:3000 --name holorepository-ui-client holorepository-ui-client:latest

# test connection (or open app in browser)
curl http://localhost/app/
```

Note that the `Dockerfile` is specified independently of the build context through the `-f` flag. This is necessary in order to copy `../types`, which would otherwise cause an error as it is outside the default build context. The build context needs to be the parent directory rather than this one.
