# Holo FHIR Tool

A tool that generates FHIR schema for HoloRepository and also inserts it into a FHIR API server.

This uses an Azure FHIR server created from the following [deployment template](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2FMicrosoft%2Ffhir-server%2Fmaster%2Fsamples%2Ftemplates%2Fdefault-azuredeploy-sql.json).

Security is disabled for development with the following additional parameter during spin up.

- "FhirServer:Security:Enabled": false

## Installation

Install using `pipenv install` or `pip install -r requirements.txt`.

## Usage

```
Usage:
    fhir_api_tool.py --base-url <FHIR_SERVER_URL> delete-all
    fhir_api_tool.py --base-url <FHIR_SERVER_URL> upload-bundle <FHIR bundle file>
    fhir_api_tool.py --base-url <FHIR_SERVER_URL> upload-bundle-folder <FHIR bundle directory>
    fhir_api_tool.py --base-url <FHIR_SERVER_URL> upload-resource <FHIR resource file>
    fhir_api_tool.py --base-url <FHIR_SERVER_URL> upload-resource-folder <FHIR resource directory>

Options:
    --base-url                  the base url of the fhir server needs to be provided (e.g. https://fhirserver.azurewebsites.net)
    delete-all                  delete all resources on the fhir server
    upload                      upload a single FHIR bundle or resource json file
    upload-folder               upload all FHIR bundles or resources stored within a folder
```
