# Azure Blob Tool

A tool that performs basic operations on the Azure Blob Storage.

## Installation

Install using `pipenv install` or `pip install -r requirements.txt`.

## Usage

_Note: You must first configure `config.cfg` with your blob storage information_

```
Usage:
    az_blob_tool.py - create-container <CONTAINER_NAME> [--public]
    az_blob_tool.py - delete-blob <CONTAINER_NAME> <FILENAME>
    az_blob_tool.py - delete-container <CONTAINER_NAME>
    az_blob_tool.py - list-blobs <CONTAINER_NAME>
    az_blob_tool.py - list-containers
    az_blob_tool.py - upload <CONTAINER_NAME> <LOCAL_FILEPATH>

Options:
    create-container    create a new container in the blob storage (default: private, add --public for public)
    delete-container    delete a container
    delete-blob         delete a blob within a container
    list-container      list all available containers
    list-blob           list all blobs within a container
    upload              upload a local file to a container
```

## Configuration

Configurations are done within `config.cfg`. Obtain the configuration values from your Azure Portal.

| Field        | Description                                   |
| ------------ | --------------------------------------------- |
| account_name | Name of azure blob storage service            |
| account_key  | Key used to access azure blob storage service |
