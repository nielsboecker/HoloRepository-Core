# Synthetic Data Modifier
A tool for modifying synthetic patient data generated as FHIR resources with [Synthea](https://github.com/synthetichealth/synthea). Certain project-specific filterings and modifications are being applied.

In particular, it does the following:
- Point selected files with imaging studies to hosted imaging studies endpoints and adjust metadata accordingly (`numberOfInstances` etc.)
- Extract Patient resource and input generalPractitioner resource to them
- Extract Practitioner resources
- Change references string format
- Discard other resources

Output data can then be uploaded into FHIR servers via the `holo_fhir_tool`.

# Installation
Install with `pipenv install`

# Configuration
```cfg
{
    "filename": [
        "study_name",
        "num_of_instances",
        "body_part_of_dicom",
        "url_to_dicom"
    ],
    ...
}
```

# Usage
```shell
synthea_data_modifier.py convert in_dir out_dir [--config config.cfg]

    convert command to convert contents in_dir to out_dir
    in_dir  path to find synthea generated data
    out_dir path to write modified data
```
