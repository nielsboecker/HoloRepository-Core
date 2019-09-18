# HoloPipelines <a href="https://dev.azure.com/MSGOSHHOLO/HoloRepository/_build/latest?definitionId=1&branchName=dev"><img src="https://dev.azure.com/MSGOSHHOLO/HoloRepository/_apis/build/status/HoloRepository-Core?branchName=dev&jobName=HoloPipelines%20-%20Core" alt="HoloPipelines core build status" align="right" /></a>

A cloud-based service that performs the automatic generation of 3D models from 2D image
stacks. Pre-trained neural network models are deployed and accessed with this component
alongside traditional techniques like Hounsfield value thresholding.

## Description

<img
src="https://user-images.githubusercontent.com/11090412/62010807-49d5b180-b167-11e9-9ff5-cd221e94b265.png"
alt="screenshot" height="350" align="left" /> The HoloPipelines are responsible for the
generation of 3D holograms to eventually be displayed in the HoloLens, sourced from
DICOM imaging studies. The cloud-hosted service provides a consistent pipeline interface
to consume DICOM and yield glTF2 files (plus associated patient data). By implementing a
Docker-based template, arbitrary pre-trained neural network (NN) models can be plugged
into the HoloPipelines service seamlessly. This allows to add new workflows in the
future and implement each workflow independently.

A typical pipeline will process the data fully automatic by utilising a NN model which
has been trained to perform a specific task, such as segmenting the bones from a CT
scan. Several Docker-based interfaces for distributing pre-trained models have been
suggested, for instance the ModelHub.ai scheme, Niftinet or Microsoft Azure ML. We will
iteratively add adapters for these interfaces, so that the HoloPipelines can integrate
existing models.

As each pipeline is independent, semi-automated or manual pipelines (which may even
include their own front-ends or manual processing steps) could be added later.

Upon receiving a DICOM image series, a job will be started and passed through the
different stages of a pipeline. The status of each job can be queried through a distinct
API. When finished, the result will be handed on to the HoloStorage Accessor.

## Technologies

Majority of the code is written in Python 3.7.3

- Web application framework to handle requests [Flask](https://github.com/pallets/flask)
- [Node.js](https://nodejs.org/en/) to utilise the package available for glTF conversion
  and transformation
- An open source convolutional neural networks platform [NiftyNet](https://niftynet.io)
- Pipelines containerized using [Docker](https://www.docker.com)
- Testing is done through [Pytest](https://github.com/pytest-dev/pytest)

## Architecture

The HoloPipelines themselves are a cloud-based application developed with Python. The
code implements a Pipes-and-Filters pattern and is kept modular. Different modules can
be pieced together to reflect different workflows, and thereby provide different
pipelines.

The modules that form a pipeline can perform different tasks:

- The first module in the chain is responsible for listening to incoming `POST` requests
  and then actively pulling the input data from the PACS.
- Intermediate modules perform various pre- or post-processing tasks such as rescaling,
  cropping, or filtering.
- Special adapter modules are used to call the pre-trained NN models, which are being
  deployed as separate containers and accessed via HTTP calls.
- The last module is responsible for sending the result off to the HoloStorage Accessor.

## Job-specific working areas

When jobs are triggered, they will automatically create and maintain their local working
 area in `<app-root-dir>/__jobs__/<job-id>`.
 
This directory contains subdirectories for `input`, `output` and `temp` data.
Furthermore, a `job.log` file contains the job-specific logs and a `job.state` file
contains the current state. The automatic garbage collection usually deletes all binary
files, but keeps logs around by default. For production deployment, this should be
changed (or the `__finished_jobs__` directory should be emptied regularly). If you want
to keep all files or change other settings, refer to the
[configuration](#configuration).

## Pre-trained NN models

We are continually wrapping existing pre-trained models with a lightweight Flask API and
a `Dockerfile`. These models can be found in the `models/` directory.

If you want to train your own model or integrate an existing model that is not
officially supported yet, you can easily integrate it yourself. You will need to
implement some kind of server to comply with the specified API endpoints (documented in
`models/README.md`) and a `Dockerfile`. You can take a look at the existing models for
reference.

## How to add new pipelines

Adding a new pipeline is fairly easy; however, it currently does include some manual
steps. The required steps vary depending on the specific use case, and on the type of
pipeline. Currently, we have three types of pipelines, that differ in the way they
perform automatic segmentation:
* Algorithmic segmentation using low-level libraries (e.g. `bone_segmentation` pipeline)
* Existing implementations of algorithmic segmentation (e.g. `lung_segmentation`
  pipeline)
* Automatic segmentation using external neural networks (e.g.
  `abdominal_organs_segmentation` pipeline)

In each case, you will have to create a new pipeline module in `./core/pipelines/`. It
should expose a `run` function (refer to existing pipelines for the signature) and be
directly invokable for testing purposes (via `__main__`). You should then also add your
pipeline to the `./core/pipelines.json` to document the pipeline's specification and
make it visible for external clients. By adding it here, it will show up as an option
for clients to run. The `job_controller` will then automatically load the new pipeline
without any code changes.

In the pipeline itself, you should only a) call other components to perform actions and
b) update the job status. Pipelines are pieced together from other components, which are
really the core building blocks of the system. For the pre- and postprocessing steps, it
is encouraged to reuse existing `tasks`, `services`, `adapters`, `wrappers` and
`clients`. If your pipeline requires other functionality, try to extract it to a
reusable components.

If you encounter an error in your component, it's okay to just raise an Error or
Exception. The `job_controller` which runs the pipelines will catch it and show an error
message. The garbage collection will clean up after you.

If you want to integrate an existing implementation in python code or need to call an
external program, write a wrapper.

If you want to integrate a pre-trained model, you should refer to `/models/README.md`
and perform the steps described to wrap the model and integrate it into the system. You
can then access it from your pipeline code.

Don't forget to update documentation, tests, and, if you add an additional external
 model, the container deployments (refer to deployment documentation).


## Development

### Requirements:

Python 3.7 or above

### Dependencies and installation:

Dependencies can be installed by using pip command as follow

```
pip install -r requirements.txt
```

Some dependencies are not available through pip, they are listed below with their
installation instructions

These 2 dependencies can be installed using Node.js package manager. Please make sure to
have the latest version of npm installed.

**obj2gltf** https://github.com/AnalyticalGraphicsInc/OBJ2GLTF

```
npm install -g obj2gltf
```

### Local development

Just start the Flask server locally. It will automatically run in debug mode, including
features like live reloading, extensive debug statements, etc.

```shell
python server.py
```

### Configuration

The application is configured through environment variables. For local development, the
`.env` file will automatically be read and the variables will be made available (Note:
`.env` file is included with test values in VCS in this case as it doesn't contain any
secrets).

In production environments, all variables in `.env` should be set by the CD workflow.

## Testing

Testing is done using pytest:

```
pip install pytest pytest-mock pytest-cov
```

Execute tests by running the following command in `HoloPipelines` directory:

```
pytest --cov
```

### Manual testing with Postman

The file `tests/HoloPipelines.postman_collection.json` contains a Postman collection
 that can be used to try out the API endpoints manually. The typical workflow is to
 trigger one of the pipelines by starting a new job (`POST /jobs`) and then tracking it
 via the `/state` and `/log` endpoints.

 Note that to test the end-to-end flow, the HoloStorageAccessor and any relevant neural
 network containers should be running as well. You can use the `docker-compose` file in
 the project root directory to help start the different sub-systems.

 ## Build and deployment

### Building and running the docker image

```shell
docker build . -t holopipelines-core
docker run --rm -p 3100:3100 --env-file .env holopipelines-core:latest
```

## API specification

```
POST /job
    Starts a new job.

GET /pipelines
    Returns a JSON list of available pipelines

GET /job/<job_id>/state
    Returns the state of a job with specific ID

GET /job/<job_id>/log
    Returns the complete log of a job with specific ID
```

## Contact and support

This component is owned by [nbckr](https://github.com/nbckr). The first prototype was
developed by [UdomkarnBoonyaprasert](https://github.com/UdomkarnBoonyaprasert) and
[ansonwong9695](https://github.com/ansonwong9695). Please get in touch if you have any
questions. For change requests and bug reports, please open a new issue.
