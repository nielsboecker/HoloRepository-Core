from unittest import mock

import os
from jobs.jobs_controller import (
    start_new_job,
    check_job_request_validity,
    create_random_job_id,
    init_job,
)
from tests.utils.input_data import sample_job


this_test_name = os.path.basename(__file__).replace(".py", "")


def test_start_new_job():
    assert start_new_job(sample_job)


def test_check_job_request_validity():
    with mock.patch("jobs.jobs_controller.init_job") as mock_init_job:
        mock_init_job.return_value = create_random_job_id()
    assert check_job_request_validity(sample_job)


def test_create_random_job_id():
    assert len(create_random_job_id()) == 16
