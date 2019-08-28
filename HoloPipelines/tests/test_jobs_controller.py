import os
from typing import Any
from unittest import mock

from pytest import fixture

from jobs.jobs_controller import (
    check_job_request_validity,
    create_random_job_id,
    start_new_job,
)
from tests.utils.input_data import sample_job


test_job_id = os.path.basename(__file__).replace(".py", "")


@fixture
def mock_init_job(mocker: Any) -> mock.MagicMock:
    """
    Mock the function that will try to start an actual job.
    """
    return mocker.patch("jobs.jobs_controller.init_job", return_value=test_job_id)


def test_start_new_job(mock_init_job: mock.MagicMock):
    result_success, result_job_response = start_new_job(sample_job)
    mock_init_job.assert_called_once()
    assert result_success is True
    assert isinstance(result_job_response, dict)
    assert isinstance(result_job_response["jid"], str)


def test_check_job_request_validity_valid():
    result, _ = check_job_request_validity(sample_job)
    assert result is True


def test_check_job_request_validity_invalid():
    result, _ = check_job_request_validity({})
    assert result is False


def test_create_random_job_id():
    result = create_random_job_id()
    assert isinstance(result, str)
    assert len(result) == 16
