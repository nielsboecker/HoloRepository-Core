# Generic neural network container
This is a simple template to create a Flask endpoint wrapped in a Docker container.

## Model deployment

```shell
# build model image
docker build -t {container-name} .

# run and map port to default HTTP port on the Docker host
docker run -p {your_port}:{your_docker_port} {container-name}:latest
```

## API specification

```
POST <container>:5000/model
  Body: <Input file according to the model's specification>
  Returns: <Output file according to the model's specification>
```

Example:

```shell
curl -X POST -F file=@{your_file} http://localhost:{your_port}/model -o output.nii.gz
```

### Testing for the flask script
You can trigger the test script inside the docker container by running the following command (make sure your container is up):
```
docker exec niftynet python3 test.py
```