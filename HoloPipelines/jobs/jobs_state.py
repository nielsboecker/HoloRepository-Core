import logging
import threading
import time
from datetime import datetime
from enum import Enum

from config import (
    KEEP_ALL_FILES,
    KEEP_ALL_LOG_FILES,
    GARBAGE_COLLECTION_INTERVAL_SECS,
    GARBAGE_COLLECTION_INACTIVE_JOB_TTL_SECS,
)
from jobs import jobs_state_dict
from jobs.jobs_io import remove_directory_for_job

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


def update_job_state(job_id: str, new_state: str, logger=logging):
    """
    Updates the global dictionary that keeps track of all jobs. Note that new_state
    must be a string, not an Enum, as the latter leads to problems with multiprocessing.
    :param job_id: ID of the job to update
    :param new_state: new state (preferably use the "name" of a JobState Enum constant)
    :param logger: optional override to the default logger (use to write to file log)
    """
    if job_id in jobs_state_dict:
        prev_state = jobs_state_dict[job_id]["state"]
        prev_timestamp = jobs_state_dict[job_id]["timestamp"]
        time_diff = (datetime.now() - prev_timestamp).total_seconds()
        logger.info(f"[{job_id}] Finished state {prev_state} in {time_diff} seconds")

    new_status_for_job = {"state": new_state, "timestamp": datetime.now()}
    logger.info(f"[{job_id}] Entering next state => {new_state}")
    jobs_state_dict[job_id] = new_status_for_job


def get_current_state(job_id: str):
    """
    :param job_id: ID of the job to query
    :return: Current <JobState.name> or False if not found
    """
    if job_id in jobs_state_dict:
        return jobs_state_dict[job_id]["state"]
    else:
        logging.warning(f"Could not get current state for job '{job_id}'")
        return False


def remove_job(job_id: str, success: bool = True):
    """
    Removes a job from the global state dict, and conditionally deletes temporary files.
    Note that this does not terminate the actual worker process of the job. In success
    cases it already finished. In error cases, the process has likely died. THere may be
    some cases of dangling processes however, and ideally we had better error handling.
    This can lead to errors which are currently not properly handled.
    :param job_id: ID of the job to remove
    :param success: True if job terminated successfully as intended, False otherwise
    """
    logging.info(f"Garbage collection | Removing job '{job_id}' (success={success})")
    jobs_state_dict.pop(job_id)

    if not KEEP_ALL_FILES:
        keep_log_file = not success or KEEP_ALL_LOG_FILES
        remove_directory_for_job(job_id, keep_log_file)


def perform_garbage_collection():
    """
    Checks the global state if any jobs have successfully terminated or have been
    inactive for a long period of time, and conditionally removes them.
    """
    while True:
        logging.info(
            f"Global state | {len(jobs_state_dict)} jobs active:"
            f" {list(jobs_state_dict.keys())}"
        )

        for job_id in list(jobs_state_dict):
            current_state = jobs_state_dict[job_id]["state"]
            current_timestamp = jobs_state_dict[job_id]["timestamp"]
            time_diff = (datetime.now() - current_timestamp).total_seconds()

            if current_state == JobState.FINISHED.name:
                remove_job(job_id, success=True)
            # After TTl seconds of unchanged status, job is considered dead and removed
            elif time_diff > int(GARBAGE_COLLECTION_INACTIVE_JOB_TTL_SECS):
                remove_job(job_id, success=False)

        time.sleep(int(GARBAGE_COLLECTION_INTERVAL_SECS))


def activate_periodic_garbage_collection():
    """
    Starts the thread which will periodically wake up and check if data can be removed.
    """
    thread = threading.Thread(target=perform_garbage_collection)
    thread.start()
    logging.info("Garbage collection | Started background thread")
