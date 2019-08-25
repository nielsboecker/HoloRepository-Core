import os
from typing import Any
from unittest import mock

import pytest

from core.pipelines import lung_segmentation
from .input_data import sample_medical_data
from .shared_fixtures import (
    patch_jobs_io_and_create_dirs,
    mock_send_to_holostorage_accessor,
)

this_test_name = os.path.basename(__file__).replace(".py", "")

imagingStudyEndpoint = (
    "https://holoblob.blob.core.windows.net/mock-pacs/normal-chest-mediastinal.zip"
)


@pytest.mark.parametrize("job_id", [this_test_name])
def test_pipeline(
    patch_jobs_io_and_create_dirs: Any,
    mock_send_to_holostorage_accessor: mock.MagicMock,
    job_id: str,
):
    lung_segmentation.run(job_id, imagingStudyEndpoint, sample_medical_data)

    mock_send_to_holostorage_accessor.assert_called_with(
        job_id=job_id, plid="lung_segmentation", medical_data=sample_medical_data
    )
