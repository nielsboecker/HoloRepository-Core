import os
import pytest
from typing import Any
from jobs.jobs_io import write_state_file_for_job, read_state_file_for_job
from jobs.jobs_state import (
    JobState,
    update_job_state,
    get_current_state,
    remove_job,
    perform_garbage_collection,
)
from tests.utils.shared_fixtures import patch_jobs_io_and_create_dirs


this_test_name = os.path.basename(__file__).replace(".py", "")


@pytest.fixture
@pytest.mark.parametrize("job_id", [this_test_name])
def create_state_file_for_testing(patch_jobs_io_and_create_dirs: Any, job_id: str):
    write_state_file_for_job(jod_id=job_id, state=JobState.CREATED.name)


@pytest.mark.parametrize("job_id", [this_test_name])
def test_update_job_state(job_id: str, create_state_file_for_testing):
    update_job_state(job_id=job_id, new_state=JobState.QUEUED.name)
    state, age = read_state_file_for_job(jod_id=job_id)
    assert state == JobState.QUEUED.name


@pytest.mark.parametrize("job_id", [this_test_name])
def test_get_current_state(job_id: str, create_state_file_for_testing):
    state, age = get_current_state(job_id=job_id)
    assert state == JobState.CREATED.name


@pytest.mark.parametrize("job_id", [this_test_name])
def test_remove_job(job_id: str, create_state_file_for_testing):
    remove_job(job_id=job_id)
    os.rmdir(f"./__test_finished_jobs__/{this_test_name}")
    is_dir_exist = os.path.isdir(this_test_name)
    assert not (is_dir_exist)
