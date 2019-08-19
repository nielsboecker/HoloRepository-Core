# HoloRepository Demo
This folder contains demo data to setup HoloRepository and the README will document the steps to spin up the necessary infrastructure for HoloRepository

## Prerequisites
- An Azure subscription

## Contents
The following describes the contents in this
It consists of fhir data for the EHR FHIR server, Storage FHIR server and some dummy holograms for the blob storage.

| Folder       | Description                                |
|--------------|--------------------------------------------|
| ehr_data     | FHIR data for the EHIR FHIR server         |
| storage_data | FHIR data for the HoloStorage FHIR server  |
| storage_glb  | Holograms for the HoloStorage Blob service |

## HoloRepository Demo Setup
### HoloStorage Blob Service
#### Setup Azure Blob Service
- Go to `Misc/Deployment/az_blob_storage`
- Configure `setup_az_blob_storage.sh`
    - Details on configuration can be found in the README.md there
- Setup azblob
    - `./setup_az_blob_storage.sh`
- Go to `portal.azure.com` and get the access key to the service

#### Hologram Data Insertion
- Go to `Misc/tools/az_blob_tool`
- Configure `config.cfg`
    - Details on configuration can be found in the README.md there
- Create `holograms` container
    - `python az_blob_tool.py - create-container holograms --public`
- Insert the demo data
    - `python az_blob_tool.py - upload-folder holograms ./../holorepo_demo_data/storage_glb`

### HoloStorage FHIR and EHR FHIR Services
#### Setup Azure FHIR service (EHR and HoloStorage)
- Go to `Misc/Deployment/az_fhir_service`
- Configure `config/ehr_fhir.cfg` and `config/holo_fhir.cfg`
    - Details on configuration can be found in the README.md there
- Setup both FHIR services
    - `./azure_fhir.sh config/ehr_fhir.cfg`
    - `./azure_fhir.sh config/holo_fhir.cfg`
- Go to `portal.azure.com` and get the FHIR urls to both services

#### FHIR Data Insertion
- Go to `Misc/tools/fhir_api_tool`
- Insert ehr data
    - `python fhir_api_tool.py --base-url <url_to_ehr_fhir> upload-folder ../../holorepo_demo_data/ehr_data`
- Insert storage data
    - `python fhir_api_tool.py --base-url <url_to_storage_fhir> upload-folder ../../holorepo_demo_data/storage_data`

