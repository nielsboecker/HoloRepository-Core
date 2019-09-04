# Holo World: How to set up a complete HoloRepository demo infrastructure
This folder contains demo data to setup HoloRepository and the README will document the steps to spin up the necessary infrastructure for HoloRepository

## Prerequisites
- An Azure subscription

## Contents
The following describes the contents provided in the demo.

It consists of FHIR data for the EHR FHIR server, Storage FHIR server and some dummy holograms for the blob storage.

| Folder       | Description                                |
|--------------|--------------------------------------------|
| ehr_data     | FHIR data for the EHIR FHIR server         |
| storage_data | FHIR data for the HoloStorage FHIR server  |
| storage_glb  | Holograms for the HoloStorage Blob service |

## HoloRepository Demo Setup
### HoloStorage Blob Service
#### Setup Azure Blob Service
- Go to `Misc/Deployment/az_blob_storage`
- Configure name and resource group in `setup_az_blob_storage.sh`
    - Additional details on configuration can be found in the tool's README.md
- Setup azblob
    - `./setup_az_blob_storage.sh`
- Go to `portal.azure.com` and get the access key to the service

#### Hologram Data Insertion
- Go to `Misc/tools/az_blob_tool`
- Configure `config.cfg`
    - Additional details on configuration can be found in the tool's README.md
- Insert the demo data
    - `python az_blob_tool.py - upload-folder holograms ../../holo_world/storage_glb`

### HoloStorage FHIR and EHR FHIR Services
#### Setup links in EHR Imaging Studies Resources
> We currently host the dicom images on our blob storage. However when it goes down, you can self host the data. DOI: 10.13140/RG.2.2.28491.95521
- For self-hosting data, change the configurations in `imagingstudy_links_change.py`
- Configure the demo ImagingStudy FHIR resource links
    - `python imagingstudy_links_change.py`

#### Setup Azure FHIR service (EHR and HoloStorage)
- Go to `Misc/Deployment/az_fhir_service`
- Configure `config/ehr_fhir.cfg` and `config/holo_fhir.cfg`
    - Additional details on configuration can be found in the tool's README.md
- Setup both FHIR services
    - `./azure_fhir.sh config/ehr_fhir.cfg`
    - `./azure_fhir.sh config/holo_fhir.cfg`
- Go to `portal.azure.com` and get the FHIR urls to both services

#### FHIR Data Insertion
- Go to `Misc/tools/fhir_api_tool`
- Insert ehr data
    - `python fhir_api_tool.py --base-url <url_to_ehr_fhir> upload-folder ../../holo_world/ehr_data`
- Insert storage data
    - `python fhir_api_tool.py --base-url <url_to_storage_fhir> upload-folder ../../holo_world/storage_data`

## HoloRepository Demo Data Breakdown
The following describes the demo data that is created for the individual services.

### Demo Imaging Studies Data in DOI: 10.13140/RG.2.2.28491.95521

| Name                                     | Type          |
|------------------------------------------|---------------|
| left-renal-mass.zip                      | DICOM         |
| left-renal-mass.zip.preview.jpg          | Preview image |
| left-scfe-pelvis-bone.zip                | DICOM         |
| left-scfe-pelvis-bone.zip.preview.jpg    | Preview image |
| left-scfe-pelvis-soft.zip                | DICOM         |
| left-scfe-pelvis-soft.zip.preview.jpg    | Preview image |
| normal-abdomen.zip                       | DICOM         |
| normal-abdomen.zip.preview.jgp           | Preview image |
| normal-chest-lung.zip                    | DICOM         |
| normal-chest-lung.zip.preview.jpg        | Preview image |
| normal-chest-mediastinal.zip             | DICOM         |
| normal-chest-mediastinal.zip.preview.jpg | Preview image |
| normal-pelvis-bone.zip                   | DICOM         |
| normal-pelvis-bone.zip.preview.jpg       | Preview image |
| normal-pelvis-soft.zip                   | DICOM         |
| normal-pelvis-soft.zip.preview.jpg       | Preview image |


> Note: Preview images must retain the `<dicom_file>.preview.jpg` syntax and hosted in the same path as the associated DICOM file.
> HoloRepository UI implicitly looks for this preview image during runtime.

### EHR FHIR Service Demo Data
| ID   | Type    | Practitioner Link | ImagingStudy Link | Description                                       |
|------|---------|-------------------|-------------------|---------------------------------------------------|
| p100 | Patient | a100 to a102      | i100 to i103      | Patient with 3 Practitioners and 4 ImagingStudies |
| p101 | Patient | a100              | i104 to i107      | Patient with 1 Practitioner and 4 ImagingStudies  |
| p102 | Patient | a100              | i108 to i110      | Patient with 1 Practitioner and 3 ImagingStudies  |
| p103 | Patient | a100              | i111 to i113      | Patient with 1 Practitioner and 3 ImagingStudies  |
| p104 | Patient | a100              | i114 to i115      | Patient with 1 Practitioner and 2 ImagingStudies  |
| p105 | Patient | a100, a102        | i116 to i117      | Patient with 2 Practitioners and 2 ImagingStudies |
| p106 | Patient | a100              | i118              | Patient with 1 Practitioners and 1 ImagingStudies |
| p107 | Patient | a100              | i119              | Patient with 1 Practitioners and 1 ImagingStudies |
| p108 | Patient | a101              | i120              | Patient with 1 Practitioners and 1 ImagingStudies |
| p109 | Patient | a101              | -                 | Patient with 1 Practitioners and 0 ImagingStudies |
| p110 | Patient | a101 to a102      | -                 | Patient with 2 Practitioners and 0 ImagingStudies |

### HoloStorage FHIR Service Demo Data
| ID   | Type              | Practitioner Link | Patient Link | Hologram File | Description      |
|------|-------------------|-------------------|--------------|---------------|------------------|
| h100 | DocumentReference | a100              | p100         | h100.glb      | Ribcage          |
| h101 | DocumentReference | a102              | p100         | h101.glb      | Lungs            |
| h102 | DocumentReference | a100              | p101         | h102.glb      | Abdomen          |
| h103 | DocumentReference | a100              | p102         | h103.glb      | Pelvis           |
| h104 | DocumentReference | a101              | p107         | h104.glb      | Airways          |
| h105 | DocumentReference | a100              | p102         | h105.glb      | Left-Scfe-Pelvis |

