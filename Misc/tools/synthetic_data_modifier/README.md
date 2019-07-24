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

# Usage
```shell
synthea_data_modifier.py convert in_dir out_dir [--config config.cfg]

    convert     command to convert contents in_dir to out_dir
    in_dir      path to find synthea generated data
    out_dir     path to write modified data
    --config    path to configuration file (default: config.cfg)
```

# Configuration
Configure specific input synthea files to be modified with specific imaging study resource information.
```cfg
{
    "filename": [
        "study_name",
        "num_of_instances",
        "body_part_of_dicom",
        "url_to_dicom"
    ],
    ...
    "patient-01.json": [
        "left-renal-mass",
        "155",
        "pelvis",
        "https://host-site/pacs/series_data.zip"
    ]
}
```

# Misc: Data Selection From Synthea
Patient data used in this module is obtained from synthea via the following steps:
1. Generate a large number of data from synthea
2. Select those containing ImagingStudy resource
3. Remove files with >750kb size
4. Pick 11 for use in the program
