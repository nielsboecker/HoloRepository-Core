import pathlib
import shutil
import os
import logging

this_comp_path = str(pathlib.Path(str(os.path.dirname(os.path.realpath(__file__)))))


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


if __name__ == "__main__":
    logging.error("component can't run on its own")
