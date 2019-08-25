import os
from typing import Any
from unittest import mock

import pytest
from pytest import fixture

from core.pipelines import abdominal_organs_segmentation
from .input_data import sample_medical_data
from .shared_fixtures import (
    patch_jobs_io_and_create_dirs,
    mock_send_to_holostorage_accessor,
)

this_test_name = os.path.basename(__file__).replace(".py", "")

imagingStudyEndpoint = (
    "https://holoblob.blob.core.windows.net/mock-pacs/normal-abdomen.zip"
)


@fixture
def mock_call_niftynet_model(mocker: Any) -> mock.MagicMock:
    """
    Mock the function that a pipeline will call to trigger Niftynet models.
    """
    mock_send_to_accessor = mocker.patch(
        "core.clients.niftynet.call_model", return_value=None, autospec=True
    )
    return mock_send_to_accessor


@pytest.mark.parametrize("job_id", [this_test_name])
@pytest.mark.skip(reason=" Niftynet step's output is needed by subsequent steps")
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
