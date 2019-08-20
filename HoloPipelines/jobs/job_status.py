import logging
import threading
import time
from datetime import datetime
from enum import Enum

from jobs import jobs_status
from jobs.jobs_io import remove_directory_for_job

JobStage = Enum(
    "JobStage",
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

# After TTl seconds of unchanged status, job is considered dead and removed
time_to_live_seconds = 30 * 60
garbage_collection_cycle_seconds = 30


def update_status(job_id: str, new_stage: str, logger=logging):
    """
    Updates the global dictionary that keeps track of all jobs. Note that new_stage
    must be a string, not an Enum, as the latter leads to problems with multiprocessing.
    :param job_id: ID of the job to update
    :param new_stage: new stage (preferably use the "name" of a JobStage Enum constant)
    :param logger: optional override to the default logger (use to write to file log)
    """
    if job_id in jobs_status:
        prev_stage = jobs_status[job_id]["stage"]
        prev_timestamp = jobs_status[job_id]["timestamp"]
        time_diff = (datetime.now() - prev_timestamp).total_seconds()
        logger.info(f"[{job_id}] Finished stage {prev_stage} in {time_diff} seconds")

    new_status_for_job = {"stage": new_stage, "timestamp": datetime.now()}
    logger.info(f"[{job_id}] Entering next stage => {new_stage}")
    jobs_status[job_id] = new_status_for_job


def get_current_stage(job_id: str):
    """
    :param job_id: ID of the job to query
    :return: Current <JobStage.name> or False if not found
    """
    if job_id in jobs_status:
        return jobs_status[job_id]["stage"]
    else:
        logging.warning(f"Could not get current stage for job '{job_id}'")
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
    jobs_status.pop(job_id)

    # TODO: Move to config / env variables
    keep_all_files = False
    keep_all_log_files = False

    if not keep_all_files:
        keep_log_file = not success or keep_all_log_files
        remove_directory_for_job(job_id, keep_log_file)


def perform_garbage_collection():
    """
    Checks the global state if any jobs have successfully terminated or have been
    inactive for a long period of time, and conditionally removes them.
    """
    while True:
        logging.info(
            f"Global state | {len(jobs_status)} jobs active:"
            f" {list(jobs_status.keys())}"
        )

        for job_id in list(jobs_status):
            current_stage = jobs_status[job_id]["stage"]
            current_timestamp = jobs_status[job_id]["timestamp"]
            time_diff = (datetime.now() - current_timestamp).total_seconds()

            if current_stage == JobStage.FINISHED.name:
                remove_job(job_id, success=True)
            elif time_diff > time_to_live_seconds:
                remove_job(job_id, success=False)

        time.sleep(garbage_collection_cycle_seconds)


def activate_periodic_garbage_collection():
    """
    Starts the thread which will periodically wake up and check if data can be removed.
    """
    thread = threading.Thread(target=perform_garbage_collection)
    thread.start()
    logging.info("Garbage collection | Started background thread")
