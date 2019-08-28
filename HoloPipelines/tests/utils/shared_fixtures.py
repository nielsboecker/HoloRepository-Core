import os
from typing import Any
from unittest import mock

from pytest import fixture

from jobs import jobs_io

test_output_path = "./__test_output__"
test_input_path = "./__test_output__"


@fixture
def create_output_directory():
    """
    Creates directory for test output data, if it does not exist yet.
    """
    os.makedirs(test_output_path, exist_ok=True)


@fixture
def create_input_directory():
    """
    Creates directory for test input data, if it does not exist yet.
    """
    os.makedirs(test_input_path, exist_ok=True)


@fixture
def patch_jobs_io_and_create_dirs(monkeypatch: Any, mocker: Any, job_id: str) -> None:
    """
    Patches jobs_io module, such that all its functions like get_log_file_path_for_job
    will prefix their paths with "__test__jobs" instead
    of "__jobs__".
    Also creates the directories for this test's job_id
    :param monkeypatch: injected by pytest
    :param job_id: id for this test job (injected by pytest when test provides as param)
    """
    monkeypatch.setattr("jobs.jobs_io.jobs_root", "./__test_jobs__")
    monkeypatch.setattr("jobs.jobs_io.finished_jobs_root", "./__test_finished_jobs__")

    jobs_io.init_create_job_state_root_directories()
    jobs_io.create_directory_for_job(job_id)


@fixture
def mock_send_to_holostorage_accessor(mocker: Any) -> mock.MagicMock:
    """
    Mock the function that a pipeline will attempt to call in order to send the
    result off to HoloStorageAccessor. Do nothing instead.
    :param mocker: injected by pytest-mock
    """
    mock_send_to_accessor = mocker.patch(
        "core.tasks.shared.dispatch_output.send_file_request_to_accessor",
        return_value=None,
        autospec=True,
    )
    return mock_send_to_accessor
