import logging
import os
import pathlib
import shutil
import uuid

from core.utils.pipelines_info import read_and_map_pipelines_info
from jobs.job_status import status

# TODO: THIS NEEDS TO BE REFACTORED
# FIXME: Fix all the issues raised in the PIPELINE/API PR, this is broken
# TODO: Do all job-related tasks in here (merge with config/io_paths?)

this_comp_path = str(pathlib.Path(str(os.path.dirname(os.path.realpath(__file__)))))
pipelines = read_and_map_pipelines_info()


def pathlib_job_path(job_ID, create_dir=True):
    job_path = pathlib.Path(this_comp_path).parents[1].joinpath("jobs", str(job_ID))
    if not os.path.exists(str(job_path)) and create_dir:
        os.mkdir(str(job_path))
    return job_path


def str_job_path(job_ID):
    return str(pathlib_job_path)


def make_str_job_path(job_ID, sub_dir_list, create_sub_directories=True):
    if (
        not os.path.isdir(str(pathlib_job_path.joinpath(*sub_dir_list).parent))
        and create_sub_directories
    ):
        os.makedirs(str(pathlib_job_path.joinpath(*sub_dir_list).parent))
    return str(pathlib_job_path.joinpath(*sub_dir_list))


def clean_up(job_ID):
    if os.path.exists(str_job_path):
        shutil.rmtree(str_job_path)


# TODO: all above is from Pap's old file, not functional at the current stage
# Below is code extracted from server
# Above needs to be fixed and married with below


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


def init_job(job_request: dict):
    job_id = create_random_job_id()
    create_directories_for_job(job_id)
    # TODO: Start the pipeline
    # TODO: Update status for job
    return job_id


def create_random_job_id():
    return str(uuid.uuid1())


def create_directories_for_job(job_id: str):
    # TODO: create the dirs
    pass


# TODO: Refactor the status structure (or replace with logging files altogether)
def get_job_status(job_id: str):
    if job_id in status:
        return True, {"status": status[job_id]["status"]}
    else:
        return False, {"message": f"Job ID '{job_id}' not found"}
