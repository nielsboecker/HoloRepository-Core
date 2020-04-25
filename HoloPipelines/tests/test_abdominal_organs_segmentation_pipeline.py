import os
import shutil
from typing import Any
from unittest import mock

import pytest
from pytest import fixture

from core.pipelines import abdominal_organs_segmentation
from jobs import jobs_io
from tests.utils.input_data import sample_medical_data
from tests.utils.shared_fixtures import (
    patch_jobs_io_and_create_dirs,
    mock_send_to_holostorage_accessor,
)

test_job_id = os.path.basename(__file__).replace(".py", "")

imagingStudyEndpoint = (
    "https://holoblob.blob.core.windows.net/mock-pacs/normal-abdomen.zip"
)


def create_mock_niftynet_output(_1: Any, _2: Any, _3: Any, _4: Any) -> None:
    """
    Copies a minimal sample Nifti dataset (from https://nifti.nimh.nih.gov/nifti-1/data)
    to the location where Niftynet would place its output in a regular run.
    """
    sample_nifti_file_path = "./tests/utils/minimal.nii.gz"
    niftynet_output_file_path = jobs_io.get_temp_file_path_for_job(
        test_job_id, "segmented.nii.gz"
    )
    shutil.copyfile(sample_nifti_file_path, niftynet_output_file_path)


@fixture
def mock_call_niftynet_model(mocker: Any) -> mock.MagicMock:
    """
    Mock the function that a pipeline will call to trigger Niftynet models.
    """
    mock_send_to_accessor = mocker.patch(
        "core.clients.niftynet.call_model",
        side_effect=create_mock_niftynet_output,
        autospec=True,
    )
    return mock_send_to_accessor


@pytest.mark.parametrize("job_id", [test_job_id])
def test_pipeline(
    patch_jobs_io_and_create_dirs: Any,
    mock_send_to_holostorage_accessor: mock.MagicMock,
    mock_call_niftynet_model: mock.MagicMock,
    job_id: str,
):
    """
    Tests the abdominal_organs_segmentation pipeline.
    Note that the Niftynet call and the HoloStorageAccessor call are mocked out.
    """
    abdominal_organs_segmentation.run(job_id, imagingStudyEndpoint, sample_medical_data)

    mock_call_niftynet_model.assert_called_once()

    mock_send_to_holostorage_accessor.assert_called_with(
        job_id=job_id,
        plid="abdominal_organs_segmentation",
        medical_data=sample_medical_data,
    )
