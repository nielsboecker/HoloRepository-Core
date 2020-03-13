"""
This module governs the jobs that are running on the HoloPipelines. It initiates
new jobs, does various checks, and performs some high-level error handling.
"""

import logging
import uuid
from multiprocessing import Pool
from typing import Tuple, Optional, Any

from config import NUM_OF_WORKER_PROCESSES
from core.pipelines.pipelines_controller import (
    get_pipelines_ids_list,
    load_pipeline_dynamically,
    get_pipeline_metadata
)
from jobs.jobs_io import create_directory_for_job, get_logger_for_job
from jobs.jobs_state import JobState, update_job_state

process_pool = Pool(NUM_OF_WORKER_PROCESSES)
logging.warning(f"Started process pool with {NUM_OF_WORKER_PROCESSES} worker processes")


def start_new_job(job_request: dict) -> Tuple[bool, dict]:
    logging.debug(f"Received request to start new job: {job_request}")

    request_is_valid, error_message = check_job_request_validity(job_request)
    if not request_is_valid:
        return False, {"message": error_message}

    job_id = init_job(job_request)
    logging.info(f"Started new job with id '{job_id}'")
    return True, {"jid": job_id}


def check_job_request_validity(job_request: dict) -> Tuple[bool, str]:
    required_keys = ["plid", "imagingStudyEndpoint", "medicalData"]
    if not all(key in job_request for key in required_keys):
        message = f"Missing keys in request: '{job_request}'"
        logging.error(message)
        return False, message

    if job_request["plid"] not in get_pipelines_ids_list():
        message = f"Invalid pipeline id: {job_request['plid']}"
        logging.error(message)
        return False, message

    return True, ""


def job_success_callback(result: Optional[Any]) -> None:
    """
    Shows success message on log. The actual cleaning up is done automatically by the
    garbage collection.

    Though the `result` variable is not used, its declaration is necessary.
    Reference: https://docs.python.org/3.4/library/multiprocessing.html?highlight=process#multiprocessing.pool.Pool.apply_async
    """
    logging.info("[SUCCESS] Job terminated successfully")


def job_error_callback(error: BaseException) -> None:
    """
    Logs an Error or Exception. This is called when any component in the job raises
    an Error or Exception. Unless they can recover themselves, it is encouraged that
    components error out and let this callback handle the error (kinda) gracefully.
    """
    logging.warning(f"[ERROR] An error occurred and caused the job to fail: {error}")


def init_job(job_request: dict) -> str:
    job_id = create_random_job_id()
    create_directory_for_job(job_id)
    logger = get_logger_for_job(job_id)
    update_job_state(job_id, JobState.CREATED.name, logger, new=True)

    pipeline_id = job_request["plid"]
    input_endpoint = job_request["imagingStudyEndpoint"]
    medical_data = job_request["medicalData"]
    pipeline_metadata = get_pipeline_metadata(pipeline_id)

    pipeline_module = load_pipeline_dynamically(pipeline_id)
    process_pool.apply_async(
        pipeline_module.run,
        args=(job_id, pipeline_metadata, input_endpoint, medical_data),
        callback=job_success_callback,
        error_callback=job_error_callback,
    )
    update_job_state(job_id, JobState.QUEUED.name, logger)
    return job_id


def create_random_job_id() -> str:
    return str(uuid.uuid4()).replace("-", "")[:16]
