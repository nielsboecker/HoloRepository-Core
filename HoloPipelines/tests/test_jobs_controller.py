from unittest import mock

from jobs.jobs_controller import (
    check_job_request_validity,
    create_random_job_id,
    start_new_job,
)
from tests.utils.input_data import sample_job


def test_start_new_job():
    result_success, result_job_response = start_new_job(sample_job)
    assert result_success is True
    assert isinstance(result_job_response, dict)
    assert isinstance(result_job_response["jid"], str)


def test_check_job_request_validity():
    with mock.patch("jobs.jobs_controller.init_job") as mock_init_job:
        mock_init_job.return_value = create_random_job_id()
    result, _ = check_job_request_validity(sample_job)
    assert result is True


def test_create_random_job_id():
    result = create_random_job_id()
    assert len(result) == 16
