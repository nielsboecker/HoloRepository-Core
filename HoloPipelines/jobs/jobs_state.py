"""
This module manages the state of current jobs and performs automatic garbage collection.
"""

import logging
import threading
import time
from enum import Enum
from typing import List, Union, Tuple

from config import (
    KEEP_ALL_FILES,
    KEEP_ALL_LOG_FILES,
    GARBAGE_COLLECTION_INTERVAL_SECS,
    GARBAGE_COLLECTION_INACTIVE_JOB_TTL_SECS,
)
from jobs.jobs_io import (
    get_all_job_subdirectory_names,
    read_state_file_for_job,
    remove_temporary_data_for_job,
    remove_log_file_for_job,
    move_job_to_finished_jobs_directory,
    write_state_file_for_job,
    state_file_for_job_exists,
)

JobState = Enum(
    "JobState",
    (
        "CREATED",
        "QUEUED",
        "STARTED",
        "FETCHING_INPUT",
        "READING_INPUT",
        "PREPROCESSING",
        "PERFORMING_SEGMENTATION",
        "POSTPROCESSING",
        "DISPATCHING_OUTPUT",
        "FINISHED",
    ),
)


def update_job_state(
    job_id: str, new_state: str, logger=logging, new: bool = False
) -> None:
    """
    Updates the state for a job by updating the job.state file. Note that new_state
    must be a string, not an Enum, as the latter leads to problems with multiprocessing.
    :param new: True if this is the first state update for a job. This is called
    before a job even enters the pipeline, while still being at the job_controller
    level; so represents the state change from <None> to JobState.CREATED
    :param job_id: ID of the job to update
    :param new_state: new state (preferably use the "name" of a JobState Enum constant)
    :param logger: optional override to the default logger (use to write to file log)
    """
    if state_file_for_job_exists(job_id) and not new:
        prev_state, prev_duration = read_state_file_for_job(job_id)
        logger.info(
            f"[{job_id}] Finished state {prev_state} in {prev_duration} seconds"
        )

    logger.info(f"[{job_id}] Entering state => {new_state}")
    write_state_file_for_job(job_id, new_state)


def get_current_state(job_id: str) -> Union[Tuple[str, float], Tuple[None, None]]:
    """
    :param job_id: ID of the job to query
    :return: Current <JobState.name> or False if not found
    """
    if state_file_for_job_exists(job_id):
        state, age = read_state_file_for_job(job_id)
        return state, age

    else:
        logging.warning(f"Could not get current state for job '{job_id}'")
        return None, None


def remove_job(job_id: str, success: bool = True) -> None:
    """
    Removes a job from the global state dict, and conditionally deletes temporary files.

    Note that this does not terminate the actual worker process of the job. In success
    cases it already finished. In error cases, the process has likely died. THere may be
    some cases of dangling processes however, and ideally we had better error handling.

    TODO: This can lead to nasty errors which are currently not properly handled. A
    finished job's directories/files may not exist any more or may have been moved.
    Late responses to still pending jobs may try to read/write files that are not
    here any more. We need to add a way to actually kill the active jobs.

    :param job_id: ID of the job to remove
    :param success: True if job terminated successfully as intended, False otherwise
    """
    logging.info(f"Garbage collection | Removing job '{job_id}' (success={success})")

    # clean up files
    if not KEEP_ALL_FILES:
        remove_temporary_data_for_job(job_id)
    if success and not KEEP_ALL_LOG_FILES:
        remove_log_file_for_job(job_id)

    # move directory (empty or with just log file remaining) to finished jobs
    move_job_to_finished_jobs_directory(job_id)


def get_list_of_active_jobs() -> List[str]:
    return get_all_job_subdirectory_names()


def perform_garbage_collection() -> None:
    """
    Checks the global state if any jobs have successfully terminated or have been
    inactive for a long period of time, and conditionally removes them.
    """
    while True:
        active_job_ids = get_list_of_active_jobs()

        logging.info(
            f"Global state | {len(active_job_ids)} jobs active: {active_job_ids}"
        )

        for job_id in active_job_ids:
            if not state_file_for_job_exists(job_id):
                # Note: To avoid errors for newly created jobs
                logging.warning(f"skipping state check for job '{job_id}'")
                continue

            state, age = read_state_file_for_job(job_id)

            if state == JobState.FINISHED.name:
                remove_job(job_id, success=True)
            # After TTl seconds of unchanged status, job is considered dead and removed
            elif age > GARBAGE_COLLECTION_INACTIVE_JOB_TTL_SECS:
                remove_job(job_id, success=False)

        time.sleep(GARBAGE_COLLECTION_INTERVAL_SECS)


def activate_periodic_garbage_collection() -> None:
    """
    Starts the thread which will periodically wake up and check if data can be removed.
    """
    thread = threading.Thread(target=perform_garbage_collection)
    thread.start()
    logging.info("Garbage collection | Started background thread")
