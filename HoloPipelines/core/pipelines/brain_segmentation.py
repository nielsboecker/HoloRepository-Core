"""
This is a pipeline performs brain segmentation using the winning network from mrbrains18 (https://doi.org/10.1007/978-3-030-11723-8_40).
"""
import os
import sys

from config import MODEL_BRAIN_SEGMENTATION_HOST, MODEL_BRAIN_SEGMENTATION_PORT
from core.adapters.nifti_file import read_nifti_as_np_array
from core.adapters.glb_file import write_mesh_as_glb
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


def run(job_id: str, pipeline_metadata: dict, input_endpoint: str, medical_data: dict) -> None:
    logger = get_logger_for_job(job_id)
    update_job_state(job_id, JobState.STARTED.name, logger)

    update_job_state(job_id, JobState.FETCHING_INPUT.name, logger)
    nifti_directory_path = get_input_directory_path_for_job(job_id)
    fetch_and_unzip(input_endpoint, nifti_directory_path)

    # TODO is unzipped file deleted or kept?
    # TODO check correct files exist in directory?

    update_job_state(job_id, JobState.PREPROCESSING.name, logger)
    # TODO perform preprocessing
    nifti_input_files_path = nifti_directory_path

    update_job_state(job_id, JobState.PERFORMING_SEGMENTATION.name, logger)
    segmented_nifti_output_file_path = get_temp_file_path_for_job(
        job_id, "segmented.nii.gz"
    )
    http.post_file(
        MODEL_BRAIN_SEGMENTATION_HOST,
        MODEL_BRAIN_SEGMENTATION_PORT,
        nifti_input_files_path,
        segmented_nifti_output_file_path,
    )

    update_job_state(job_id, JobState.POSTPROCESSING.name, logger)
    segmented_array = read_nifti_as_np_array(
        segmented_nifti_output_file_path, normalise=False
    )

    # transform numpy matrix according to metadata dict
    segmented_array = seperate_segmentation(segmented_array)

    obj_output_path = get_result_file_path_for_job(job_id)
    # TODO add metadata and test this
    write_mesh_as_glb(segmented_array, obj_output_path)

    update_job_state(job_id, JobState.DISPATCHING_OUTPUT.name, logger)
    dispatch_output(job_id, this_plid, medical_data)

    update_job_state(job_id, JobState.FINISHED.name, logger)


if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2], sys.argv[3])
