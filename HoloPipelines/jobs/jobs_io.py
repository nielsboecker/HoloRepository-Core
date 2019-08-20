import logging
import os

import coloredlogs

job_directories_root = "./__jobs__"
job_subdirectories = ["input", "temp", "output"]


def get_directory_path_for_job(job_id: str):
    return f"{job_directories_root}/{job_id}"


def get_temp_file_path_for_job(job_id: str, file_name: str):
    return f"{job_directories_root}/{job_id}/temp/{file_name}"


def create_directory_for_job(job_id: str):
    logging.warning(f"Creating directory for job '{job_id}'")
    job_directory_path = get_directory_path_for_job(job_id)
    os.makedirs(job_directory_path, exist_ok=True)

    for subdirectory_name in job_subdirectories:
        subdirectory_path = f"{job_directory_path}/{subdirectory_name}"
        if not os.path.isdir(subdirectory_path):
            os.mkdir(subdirectory_path)


def get_logger_for_job(job_id: str):
    log_format_console = "%(asctime)s | %(name)s | %(levelname)-5s | %(message)s"
    log_format_file = "%(asctime)s | %(levelname)-5s | %(message)s"
    coloredlogs.install(level=logging.DEBUG, fmt=log_format_console)

    logger = logging.getLogger(job_id)
    logger.setLevel(logging.DEBUG)

    # Append file handler to save log to file in addition to console output
    # (do not manually add a console handler, to use default coloredlogs output)
    fh = logging.FileHandler(f"{get_directory_path_for_job(job_id)}/job.log")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter(fmt=log_format_file))
    logger.addHandler(fh)

    return logger
