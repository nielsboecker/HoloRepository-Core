# Setup Azure FHIR Service

Script that setups a FHIR service on Azure using Microsoft's deployment template.

Reference:
https://azure.microsoft.com/en-in/blog/microsoft-fhir-server-for-azure-extends-to-sql/

## Prerequisites

- [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)

## Usage

```
Usage:
    ./azure_fhir.sh <PATH_TO_CONFIG>
```

## Configuration

| Field             | Description                                         |
| ----------------- | --------------------------------------------------- |
| RESOURCE_GROUP    | Azure resource group name to deploy into            |
| RESOURCE_LOCATION | Azure deployment location name (e.g. uksouth)       |
| SERVICE_NAME      | Name of your FHIR service                           |
| SQL_PASSWORD      | Password of the SQL server used in the FHIR backend |
