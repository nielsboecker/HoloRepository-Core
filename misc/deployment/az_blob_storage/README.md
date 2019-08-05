# Setup Azure Blob Storage

Script that setups an Azure blob storage instance.

## Prerequsites

- [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)

## Usage

_Note: Configuration fields are within the script itself_

```
Usage:
    ./setup_az_blob_storage.sh
```

## Configuration

| Field           | Description                                         |
| --------------- | --------------------------------------------------- |
| RES_GRP         | Name of azure resource group to deploy into         |
| LOC             | Location of resource group                          |
| BLOB_STORE_NAME | Name of blog storage                                |
| CONTAINERS      | List of containers that will be created after setup |
