import logging
import uuid
from multiprocessing import Pool
from os import cpu_count

from core.pipelines.bone_segmentation import main
from core.utils.pipelines_info import read_and_map_pipelines_info
from jobs.job_status import status
from jobs.jobs_io import create_directory_for_job

pipelines = read_and_map_pipelines_info()

num_cpus = cpu_count()
process_pool = Pool(num_cpus)
logging.warning(f"Started process pool with {num_cpus} worker processes")


def start_new_job(job_request: dict):
    logging.debug(f"Received request to start new job: {job_request}")

    request_is_valid, error_message = check_job_request_validity(job_request)
    if not request_is_valid:
        return False, {"message": error_message}

    job_id = init_job(job_request)
    logging.info(f"Started new job with id '{job_id}'")
    return True, {"jid": job_id}


def check_job_request_validity(job_request: dict):
    required_keys = ["plid", "imagingStudyEndpoint", "medicalData"]
    if not all(key in job_request for key in required_keys):
        message = f"Missing keys in request: '{job_request}'"
        logging.error(message)
        return False, message

    if job_request["plid"] not in pipelines.keys():
        message = f"Invalid pipeline id: {job_request['plid']}"
        logging.error(message)
        return False, message

    return True, ""


def job_success_callback(result):
    logging.info(">>> SUCCESS")
    logging.warning(result)


def job_error_callback(exception):
    logging.info(">>> ERROR")
    logging.warning(exception)


def init_job(job_request: dict):
    job_id = create_random_job_id()
    create_directory_for_job(job_id)

    input_endpoint = job_request["imagingStudyEndpoint"]
    medical_data = job_request["medicalData"]

    process_pool.apply_async(
        main,
        args=(job_id, input_endpoint, medical_data),
        callback=job_success_callback,
        error_callback=job_error_callback,
    )

    # TODO: dynamic loading?
    # TODO: Update status for job
    return job_id


def create_random_job_id():
    return str(uuid.uuid4()).replace("-", "")[:10]


# TODO: Refactor the status structure (or replace with logging files altogether)
def get_job_status(job_id: str):
    if job_id in status:
        return True, {"status": status[job_id]["status"]}
    else:
        return False, {"message": f"Job ID '{job_id}' not found"}
