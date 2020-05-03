"""
This is a pipeline performs brain segmentation using the winning network from mrbrains18 (https://doi.org/10.1007/978-3-030-11723-8_40).
"""
import os
import sys

from config import MODEL_BRAIN_SEGMENTATION_HOST, MODEL_BRAIN_SEGMENTATION_PORT
from core.adapters.nifti_file import read_nifti_as_np_array
from core.adapters.glb_file import write_mesh_as_glb
from core.services.marching_cubes import generate_mesh
from core.services.np_image_manipulation import seperate_segmentation
from core.clients import http
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
    nifti_directory_path = get_input_directory_path_for_job(job_id)
    fetch_and_unzip(input_endpoint, nifti_directory_path)
    # TODO check correct files exist in directory?
    # TODO for testing append folder name, should extract files into different path, need to change unzip
    nifti_input_files_path = os.path.join(nifti_directory_path, "brain_segmentation")

    update_job_state(job_id, JobState.PREPROCESSING.name, logger)

    update_job_state(job_id, JobState.PERFORMING_SEGMENTATION.name, logger)
    segmented_nifti_output_file_path = get_temp_file_path_for_job(
        job_id, "segmented.nii.gz"
    )
    http.post_files(
        MODEL_BRAIN_SEGMENTATION_HOST,
        MODEL_BRAIN_SEGMENTATION_PORT,
        nifti_input_files_path,
        segmented_nifti_output_file_path,
    )

    update_job_state(job_id, JobState.POSTPROCESSING.name, logger)
    segmented_array = read_nifti_as_np_array(
        segmented_nifti_output_file_path, normalise=True
    )

    # TODO for now just use two of the segments
    meshes = [
        generate_mesh(segment, 0)
        for segment in seperate_segmentation(segmented_array, unique_values=[1, 4])
    ]

    obj_output_path = get_result_file_path_for_job(job_id)
    # TODO do something for colours
    colours = [[0, 0.3, 1.0, 0.2], [1.0, 1.0, 0.0, 1.0]]
    # TODO add metadata?
    write_mesh_as_glb(meshes, obj_output_path, colours)

    update_job_state(job_id, JobState.DISPATCHING_OUTPUT.name, logger)
    dispatch_output(job_id, this_plid, medical_data)

    update_job_state(job_id, JobState.FINISHED.name, logger)


if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2], sys.argv[3])
