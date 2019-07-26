# HoloStorage Accessor
This is the accessor that provides a RESTful interface to manage all data flows going in and out of the HoloStorage.

The APIs are designed and documented via OpenAPI. Server boilerplate was generated via openapi-generator.

# Requirements
TODO

# Usage
## Running the server

To run the server, follow these simple steps:

```
go run main.go
```

To run the server in a docker container
```
docker build --network=host -t openapi .
```

Once the image is built, just run
```
docker run --rm -it openapi
```
