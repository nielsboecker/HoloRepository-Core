# HoloPipelines-Models <a href="https://dev.azure.com/MSGOSHHOLO/HoloRepository/_build/latest?definitionId=1&branchName=dev"><img src="https://dev.azure.com/MSGOSHHOLO/HoloRepository/_apis/build/status/HoloRepository-Core?branchName=dev&jobName=HoloPipelines%20-%20Models" alt="HoloPipelines models build status" align="right" /></a>

This directory contains pre-trained models which have been wrapped with a lightweight server and a `Dockerfile`. They can easily be ran and perform the specific tasks they were trained to do, for instance segmenting a particular organ.

Any further models to be supported should comply with the same API. Any server technology may be used, as long as the `Dockerfile` exposes the same endpoints and has the expected behaviour. If a new model is added to this directory, please add the description to the [Overview](#models-overview) section in this document.

Within the HoloPipelines code, an adapter should access the model. If the models I/O is similar to an existing model, the adapter may be reused. Otherwise, a new adapter should be added.

## API specification

```
POST <container>:5000/model
  Body: <Input file according to the model's specification>
  Returns: <Output file according to the model's specification>
```

Example:

```shell
curl -X POST -F file=@100_CT.nii http://localhost:5000/model -o output.nii.gz
```

## Model deployment

```shell
# build model image
docker build -t my-model .

# run and map port to default HTTP port on the Docker host
docker run -p 80:5000 my-model:latest
```

## Models overview

### [dense_vnet_abdominal_ct](https://github.com/nbckr/HoloRepository-Core/tree/master/HoloPipelines/models/dense_vnet_abdominal_ct)

Automatic multi-organ segmentation on abdominal CT with dense v-networks. This network segments eight organs on abdominal CT, comprising the gastointestinal tract (esophagus, stomach, duodenum), the pancreas, and nearby organs (liver, gallbladder, spleen, left kidney).
**\[[Source](https://github.com/NifTK/NiftyNetModelZoo/blob/master/dense_vnet_abdominal_ct_model_zoo.md)\]**
