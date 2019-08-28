"""
This module contains functionality concerned with I/O of jobs. Throughout its
life-cycle, a job creates its own working area on disk where it stores input
data, intermediate results, and ouput data.

Node that job-specific data is transient. After a job is finished, data will
be cleaned up through automatic garbage collection (unless configured otherwise).
"""

import logging
import os
import shutil
import time
from typing import List, Tuple, Optional, Union

import coloredlogs

jobs_root = "./__jobs__"
finished_jobs_root = "./__finished_jobs__"
subdirectories_per_job = ["input", "temp", "output"]


def get_directory_path_for_job(job_id: str) -> str:
    return f"{jobs_root}/{job_id}"


def get_subdirectories_paths_for_job(job_id: str) -> List[str]:
    job_directory_path = get_directory_path_for_job(job_id)
    return [
        f"{job_directory_path}/{subdirectory_name}"
        for subdirectory_name in subdirectories_per_job
    ]


def get_temp_file_path_for_job(job_id: str, file_name: str) -> str:
    return f"{jobs_root}/{job_id}/temp/{file_name}"


def get_result_file_path_for_job(job_id: str) -> str:
    return f"{jobs_root}/{job_id}/output/out.glb"


def get_input_directory_path_for_job(job_id: str) -> str:
    return f"{jobs_root}/{job_id}/input"


def init_create_job_state_root_directories() -> None:
    logging.info("Creating job state root directories")
    os.makedirs(jobs_root, exist_ok=True)
    os.makedirs(finished_jobs_root, exist_ok=True)


def create_directory_for_job(job_id: str) -> None:
    logging.info(f"Creating directory for job '{job_id}'")
    job_directory_path = get_directory_path_for_job(job_id)
    os.makedirs(job_directory_path, exist_ok=True)

    for subdirectory_path in get_subdirectories_paths_for_job(job_id):
        if not os.path.isdir(subdirectory_path):
            os.makedirs(subdirectory_path, exist_ok=True)


def move_job_to_finished_jobs_directory(job_id: str) -> None:
    old_path = get_directory_path_for_job(job_id)
    new_path = old_path.replace(jobs_root, finished_jobs_root)

    # Handle edge cases where new_path already exists
    if os.path.isdir(new_path):
        shutil.rmtree(new_path)

    logging.info(f"Moving '{old_path}' to '{new_path}'")
    shutil.move(old_path, new_path)


def remove_temporary_data_for_job(job_id: str) -> None:
    """
    Removes all transient job data except for the log file.
    """
    logging.info(f"Removing temporary files for job '{job_id}")
    try:
        # input, output, temp
        for subdirectory_path in get_subdirectories_paths_for_job(job_id):
            shutil.rmtree(subdirectory_path)

        # job.state
        os.remove(get_state_file_path_for_job(job_id))
    except FileNotFoundError as e:
        # Can happen if another worker process already removed this
        logging.warning(f"Error while removing: {e}")


def remove_log_file_for_job(job_id: str) -> None:
    logging.info(f"Removing log file for job '{job_id}")
    os.remove(get_log_file_path_for_job(job_id))


def get_all_job_subdirectory_names() -> List[str]:
    return [dir.name for dir in os.scandir(jobs_root) if dir.is_dir()]


def read_state_file_for_job(jod_id: str) -> Union[Tuple[str, float], Tuple[None, None]]:
    """
    Reads state file and returns state and time in seconds since last modification.
    """
    state_file_path = get_state_file_path_for_job(jod_id)

    try:
        with open(state_file_path, "r") as state_file:
            state = state_file.read()

        modified_time_epoch_seconds = os.path.getmtime(state_file_path)
        now_epoch_seconds = time.time()
        return state, now_epoch_seconds - modified_time_epoch_seconds
    except FileNotFoundError as e:
        logging.warning(f"State file error: '{e}''")
        return None, None


def state_file_for_job_exists(job_id: str) -> bool:
    return os.path.exists(get_state_file_path_for_job(job_id))


def write_state_file_for_job(jod_id: str, state: str) -> None:
    state_file_path = get_state_file_path_for_job(jod_id)

    try:
        with open(state_file_path, "w") as state_file:
            state_file.write(state)
    except FileNotFoundError as e:
        # handle rare errors where state would be changed after moving to finished jobs
        logging.warning(f"Ignoring attempt to update state: {e}")


def get_logger_for_job(job_id: str) -> logging.Logger:
    log_format_console = "%(asctime)s | %(name)s | %(levelname)-5s | %(message)s"
    log_format_file = "%(asctime)s | %(levelname)-5s | %(message)s"
    coloredlogs.install(level=logging.DEBUG, fmt=log_format_console)

    logger = logging.getLogger(job_id)
    logger.setLevel(logging.DEBUG)

    # Append file handler to save log to file in addition to console output
    # (do not manually add a console handler, to use default coloredlogs output)
    handler = logging.FileHandler(get_log_file_path_for_job(job_id))
    fh = handler
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter(fmt=log_format_file))
    logger.addHandler(fh)

    return logger


def get_log_file_path_for_job(job_id: str) -> Optional[str]:
    """
    Returns the path to a log file.
    :param finished: check in finished jobs directory instead of regular
    """
    path = get_directory_path_for_job(job_id)

    if os.path.isdir(path):
        return f"{path}/job.log"
    elif os.path.isdir(path.replace(jobs_root, finished_jobs_root)):
        return f"{path.replace(jobs_root, finished_jobs_root)}/job.log"
    else:
        return None


def get_state_file_path_for_job(job_id: str) -> str:
    return f"{get_directory_path_for_job(job_id)}/job.state"


def read_log_file_for_job(job_id: str) -> str:
    """
    :return: the complete log for a specific job as text or empty string
    """
    log_path = get_log_file_path_for_job(job_id)
    if not os.path.exists(log_path):
        # Try falling back on finished jobs
        log_path = get_log_file_path_for_job(job_id)
    if not log_path:
        logging.warning(f"No log found for '{job_id}'")
        return ""

    with open(log_path, "r") as log_file:
        return log_file.read()
