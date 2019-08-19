import json
import logging
import os
import pathlib
import shutil

# TODO: THIS NEEDS TO BE REFACTORED
# FIXME: Fix all the issues raised in the PIPELINE/API PR, this is broken
# TODO: Do all job-related tasks in here (merge with config/io_paths?)
import uuid
from datetime import datetime

from core.utils.pipelines_info import read_and_map_pipelines_info
from jobs.job_status import status
from pipeline_runner import startPipeline

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
    request_is_valid = check_job_request_validity(job_request)
    if not request_is_valid:
        return False, {"message": "Error while trying to start new job"}

    init_job(job_request)

    request_plid = job_request["plid"]

    meta_data_keys = ["bodySite", "description", "author", "patient"]
    meta_data = {key: job_request[key] for key in meta_data_keys}
    meta_data["dateOfImaging"] = datetime.strptime(
        job_request["dateOfImaging"], "%Y-%m-%d %H:%M:%S"
    ).strftime("%Y-%m-%dT%H:%M:%SZ")
    logging.info("meta_data: " + json.dumps(meta_data))

    # create arglist pass to pipeline controller
    # (this part will change later, we should not check the pipeline arglist in this way)
    jobID = str(uuid.uuid1())
    arg_dict = {
        "job_ID": jobID,
        # "dicom_download_url": request_input_data_URL,
        "meta_data": json.dumps(meta_data),
    }
    logging.info("arg_dict: " + str(arg_dict))

    # pass to controller to start pipeline
    startPipeline(request_plid, arg_dict)
    return True, {"jobID": jobID}


def check_job_request_validity(job_request: dict):
    if "plid" not in job_request or job_request["plid"] not in pipelines.keys():
        logging.error(f"Invalid pipeline id in request: '{job_request}'")
        return False

    required_keys = [
        "imageStudyEndpoint",
        "bodySite",
        "description",
        "author",
        "patient",
        "dateOfImaging",
    ]
    if not all(key in job_request for key in required_keys):
        logging.error(f"Missing keys in request: '{job_request}'")
        return False


def init_job(job_request: dict):
    job_id = create_random_job_id()
    create_directories_for_job(job_id)


def create_random_job_id():
    return str(uuid.uuid1())


def create_directories_for_job(job_id: str):
    pass


# TODO: Refactor the status structure (or replace with logging files altogether)
def get_job_status(job_id: str):
    if job_id in status:
        return True, {"status": status[job_id]["status"]}
    else:
        return False, {"message": f"Job ID '{job_id}' not found"}
