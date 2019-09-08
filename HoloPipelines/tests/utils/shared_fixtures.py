import os
from typing import Any
from unittest import mock
import shutil

from pytest import fixture

from jobs import jobs_io

test_jobs_dir_path = "./__test_jobs__"
test_finished_jobs_dir_path = "./__test_finished_jobs__"
test_output_directory_path = "./__test_output__"
test_input_directory_path = "./__test_output__"


@fixture
def create_output_directory():
    """
    Creates directory for test output data, if it does not exist yet.
    """
    os.makedirs(test_output_directory_path, exist_ok=True)


@fixture
def create_input_directory():
    """
    Creates directory for test input data, if it does not exist yet.
    """
    os.makedirs(test_input_directory_path, exist_ok=True)


@fixture(scope="session", autouse=True)
def create_and_delete_test_output_directory():
    """
    Creates test output directory before first test in session, and deletes it after
    the last test ran.
    """
    os.makedirs(test_output_directory_path, exist_ok=True)
    yield

    shutil.rmtree(test_output_directory_path)


@fixture
def patch_jobs_io_and_create_dirs(monkeypatch: Any, job_id: str) -> None:
    """
    Patches jobs_io module, such that all its functions like get_log_file_path_for_job
    will prefix their paths with "__test__jobs" instead
    of "__jobs__".
    Also creates the directories for this test's job_id
    :param monkeypatch: injected by pytest
    :param job_id: id for this test job (injected by pytest when test provides as param)
    """
    monkeypatch.setattr("jobs.jobs_io.jobs_root", test_jobs_dir_path)
    monkeypatch.setattr("jobs.jobs_io.finished_jobs_root", test_finished_jobs_dir_path)

    jobs_io.init_create_job_state_root_directories()
    jobs_io.create_directory_for_job(job_id)


@fixture
def mock_send_to_holostorage_accessor(mocker: Any) -> mock.MagicMock:
    """
    Mock the function that a pipeline will attempt to call in order to send the
    result off to HoloStorageAccessor. Do nothing instead.
    :param mocker: injected by pytest-mock
    """
    return mocker.patch(
        "core.tasks.shared.dispatch_output.send_file_request_to_accessor",
        return_value=None,
        autospec=True,
    )
