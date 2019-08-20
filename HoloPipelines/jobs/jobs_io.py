import logging
import os
import shutil

import coloredlogs

job_directories_root = "./__jobs__"
job_subdirectories = ["input", "temp", "output"]


def get_directory_path_for_job(job_id: str):
    return f"{job_directories_root}/{job_id}"


def get_subdirectories_paths_for_job(job_id: str):
    job_directory_path = get_directory_path_for_job(job_id)
    return [
        f"{job_directory_path}/{subdirectory_name}"
        for subdirectory_name in job_subdirectories
    ]


def get_temp_file_path_for_job(job_id: str, file_name: str):
    return f"{job_directories_root}/{job_id}/temp/{file_name}"


def get_result_file_path_for_job(job_id: str):
    return f"{job_directories_root}/{job_id}/output/out.glb"


def get_input_directory_path_for_job(job_id: str):
    return f"{job_directories_root}/{job_id}/input"


def create_directory_for_job(job_id: str):
    logging.info(f"Creating directory for job '{job_id}'")
    job_directory_path = get_directory_path_for_job(job_id)
    os.makedirs(job_directory_path, exist_ok=True)

    for subdirectory_path in get_subdirectories_paths_for_job(job_id):
        if not os.path.isdir(subdirectory_path):
            os.mkdir(subdirectory_path)


def remove_directory_for_job(job_id: str, keep_log_file: bool = True):
    logging.info(f"Removing files for job '{job_id} (keep_log_file={keep_log_file})'")
    job_directory_path = get_directory_path_for_job(job_id)
    if keep_log_file:
        for subdirectory_path in get_subdirectories_paths_for_job(job_id):
            shutil.rmtree(subdirectory_path)
    else:
        shutil.rmtree(job_directory_path)


def get_logger_for_job(job_id: str):
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


def get_log_file_path_for_job(job_id: str):
    return f"{get_directory_path_for_job(job_id)}/job.log"


def read_log_file_for_job(job_id: str):
    """
    :return: the complete log for a specific job as text or empty string
    """
    log_path = get_log_file_path_for_job(job_id)
    if not os.path.exists(log_path):
        return ""

    with open(log_path, "r") as log_file:
        return log_file.read()
