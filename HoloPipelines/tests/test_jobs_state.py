import os
import pytest
from typing import Any
from jobs.jobs_io import (
    write_state_file_for_job,
    read_state_file_for_job,
    get_directory_path_for_job,
)
from jobs.jobs_state import JobState, update_job_state, get_current_state, remove_job
from tests.utils.shared_fixtures import (
    test_finished_jobs_dir_path,
    patch_jobs_io_and_create_dirs,
)


test_job_id = os.path.basename(__file__).replace(".py", "")


@pytest.fixture
def create_state_file_for_testing(patch_jobs_io_and_create_dirs: Any, job_id: str):
    """
    Creates a state file in the test jobs directory for a given job id.
    """
    write_state_file_for_job(jod_id=job_id, state=JobState.CREATED.name)


@pytest.mark.parametrize("job_id", [test_job_id])
def test_update_job_state(job_id: str, create_state_file_for_testing):
    update_job_state(job_id=job_id, new_state=JobState.QUEUED.name)
    state, age = read_state_file_for_job(jod_id=job_id)
    assert state == JobState.QUEUED.name
    assert isinstance(age, float)


@pytest.mark.parametrize("job_id", [test_job_id])
def test_get_current_state(job_id: str, create_state_file_for_testing):
    state, age = get_current_state(job_id=job_id)
    assert state == JobState.CREATED.name
    assert isinstance(age, float)


@pytest.mark.parametrize("job_id", [test_job_id])
def test_remove_job(job_id: str, create_state_file_for_testing):
    assert os.path.isdir(get_directory_path_for_job(test_job_id))

    remove_job(job_id=job_id)
    assert not os.path.isdir(get_directory_path_for_job(test_job_id))
    assert os.path.isdir(f"{test_finished_jobs_dir_path}/{test_job_id}")
