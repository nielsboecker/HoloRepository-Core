# Synthetic Data Modifier
Tool used will modify synthea generated fhir data to what is needed for the project.

It does the following:
- Point selected files with imaging studies to hosted imaging studies endpoints,
- Extract Patient resource and input generalPractitioner resource to them
- Extract Practitioner resources

Output data can then be uploaded into FHIR servers via the "holo_fhir_tool".

# Installation
Install with `pipenv install`

# Configuration
"""
{
    "filename": [
        "study_name",
        "num_of_instances",
        "body_part_of_dicom",
        "url_to_dicom"
    ],
    ...
}
"""

# Usage
Usage:       synthea_data_modifier.py convert in_dir out_dir [--config config.cfg]

    convert command to convert contents in_dir to out_dir
    in_dir  path to find synthea generated data
    out_dir path to write modified data
