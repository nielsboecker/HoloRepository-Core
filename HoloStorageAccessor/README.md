# HoloStorageAccessor <a href="https://dev.azure.com/MSGOSHHOLO/HoloRepository/_build/latest?definitionId=1&branchName=dev"><img src="https://dev.azure.com/MSGOSHHOLO/HoloRepository/_apis/build/status/HoloRepository-Core?branchName=dev&jobName=HoloStorageAccessor" alt="HoloStorageAccessor build status" align="right" /></a>

The HoloStorage is a cloud-based storage for medical 3D models and associated metadata. Entirely hosted on Microsoft Azure, a FHIR server stores the structured medical data and a Blob Storage server provides for the binary holographic data. With the HoloStorageAccessor, we provide an enhanced facade, offering a consistent interface to the HoloStorage and translating the public REST API to internal FHIR queries. To facilitate development of 3rd party components, the interface comes with an interactive OpenAPI documentation.

## Description

<img src="https://user-images.githubusercontent.com/11090412/62010808-49d5b180-b167-11e9-9ce7-7335aa616926.png" alt="screenshot" height="350" align="left" />
To protect the HoloStorage and hide concrete implementation details, such as which FHIR resources are used to store data internally, the HoloStorage-Accessor provides a consistent and unified interface to the data, and the single entry-point for 3rd party systems. As such, it acts as a façade. However, it also performs some more complex business logic, like translating calls to a minimalistic interface to FHIR queries and building complex queries, potentially filtering and aggregating results.

The REST API is being carefully designed, so that it not only satisfies the requirements of the HoloPipelines’ artefacts, but also supports adjacent projects (DepthVisor, Annotator) and any future projects in this context. We strive to find a balance between an open, generic interface and enforcing enough relevant data to effectively query and utilise the data.
## Technologies

The following technologies are used in this component:

- Go 1.12.7
- API specification using [OpenAPI v3.0.2](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md)
- Backend implementation using [Go Gin framework](https://github.com/gin-gonic/gin)
- Server stub generated from OpenAPI specifications using [OpenAPI Generator](https://openapi-generator.tech/)

## API specification

The API specification can be found in the `api/` directory. A deployed version of the interactive documentation is available [here](https://app.swaggerhub.com/apis/boonwj/HoloRepository/).

When the application is deployed, the documentation can also be viewed at the `/api/1.0.0/ui` endpoint.

## Requirements
- Go 1.12.7

## Development
### Installation
To install program dependencies

```
go get -d -v ./...
```

### Run

To run the server, first configure the necessary [configurations](#configuration) then run the following

```
go run cmd/holo-storage-accessor/main.go
```

Verify the accessor is running

```
curl localhost:8080/api/1.0.0/
```


### Testing

To run the tests

```
go test ./...
```

## Build and deployment

To run the server in a docker container

```
docker build -t holo-storage-accessor .
```

Once the image is built load the configuration, just run

```
docker run -it --rm --env-file config.env -p 8080:8080 holo-storage-accessor
```
You can then access the container via localhost:8080

## Configuration
Accessor application uses the following environmental variables as configuration.

If using docker, the environment configuration fields can be set via `config.env`.

If not, `export` the variables before running the program.

| Field                    | Description                                      |
|--------------------------|--------------------------------------------------|
| ACCESSOR_FHIR_URL        | URL to the FHIR server that accessor connects to |
| AZURE_STORAGE_ACCOUNT    | Name of blob store for holograms                 |
| AZURE_STORAGE_ACCESS_KEY | Access key to the blob store                     |


## Contact and support

This component is owned by [boonwj](https://github.com/boonwj). Please get in touch if you have any questions. For change requests and bug reports, please open a new issue.
