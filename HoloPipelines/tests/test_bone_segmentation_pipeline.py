import os

import pytest

from core.pipelines import bone_segmentation
from ._input_utils import sample_medical_data
from ._fixtures import patch_jobs_io_and_create_dirs  # noqa: F401

this_test_name = os.path.basename(__file__).replace(".py", "")

imagingStudyEndpoint = (
    "https://holoblob.blob.core.windows.net/mock-pacs/normal-chest" "-mediastinal.zip"
)


@pytest.mark.parametrize("job_id", [this_test_name])
def test_pipeline(patch_jobs_io_and_create_dirs, job_id):  # noqa: F811
    bone_segmentation.run(job_id, imagingStudyEndpoint, sample_medical_data)
