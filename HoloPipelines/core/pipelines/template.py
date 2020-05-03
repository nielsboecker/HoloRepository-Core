"""
This is a template file to be used when creating a new pipeline.
"""
import os
import sys
import numpy as np

from core.adapters.dicom_file import read_dicom_as_np_ndarray_and_normalise
from core.adapters.glb_file import convert_obj_to_glb_and_write
from core.adapters.obj_file import write_mesh_as_obj
from core.services.marching_cubes import generate_mesh
from core.services.np_image_manipulation import downscale_and_conditionally_crop
from core.tasks.shared.dispatch_output import dispatch_output
from core.tasks.shared.receive_input import fetch_and_unzip
from jobs.jobs_io import (
    get_input_directory_path_for_job,
    get_logger_for_job,
    get_result_file_path_for_job,
    get_temp_file_path_for_job,
)
from jobs.jobs_state import JobState, update_job_state

this_plid = os.path.basename(__file__).replace(".py", "")


def run(job_id: str, input_endpoint: str, medical_data: dict) -> None:
    logger = get_logger_for_job(job_id)
    update_job_state(job_id, JobState.STARTED.name, logger)

    update_job_state(job_id, JobState.FETCHING_INPUT.name, logger)
    dicom_directory_path = get_input_directory_path_for_job(job_id)
    fetch_and_unzip(input_endpoint, dicom_directory_path)

    update_job_state(job_id, JobState.READING_INPUT.name, logger)
    dicom_image: np.ndarray = read_dicom_as_np_ndarray_and_normalise(
        dicom_directory_path
    )

    update_job_state(job_id, JobState.PREPROCESSING.name, logger)
    downscaled_image = downscale_and_conditionally_crop(dicom_image)

    update_job_state(job_id, JobState.PERFORMING_SEGMENTATION.name, logger)
    # Insert segmentation here

    update_job_state(job_id, JobState.POSTPROCESSING.name, logger)
    verts, faces, norm = generate_mesh(downscaled_image, 0)
    obj_output_path = get_temp_file_path_for_job(job_id, "temp.obj")
    write_mesh_as_obj(verts, faces, norm, obj_output_path)
    convert_obj_to_glb_and_write(obj_output_path, get_result_file_path_for_job(job_id))

    update_job_state(job_id, JobState.DISPATCHING_OUTPUT.name, logger)
    dispatch_output(job_id, this_plid, medical_data)

    update_job_state(job_id, JobState.FINISHED.name, logger)


if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2], sys.argv[3])
