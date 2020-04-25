"""
This pipeline performs automatic segmentation of lungs. It uses an existing algorithmic
implementation for the actual segmentation.

Algorithm: https://github.com/wanwanbeen/ct_lung_segmentation
Paper: Discriminative Localization in CNNs for Weakly-Supervised Segmentation of Pulmonary Nodules
Xinyang Feng, Jie Yang, Andrew F. Laine, Elsa D. Angelini
"""

import os
import sys

from core.adapters.dicom_file import read_dicom_as_np_ndarray_and_normalise

from core.adapters.nifti_file import (
    convert_dicom_np_ndarray_to_nifti_image,
    read_nifti_as_np_array,
    write_np_array_as_nifti_image,
)
from core.adapters.glb_file import write_mesh_as_glb
from core.services.marching_cubes import generate_mesh
from core.services.np_image_manipulation import downscale_and_conditionally_crop
from core.tasks.shared.dispatch_output import dispatch_output
from core.tasks.shared.receive_input import fetch_and_unzip
from core.third_party.lung_and_airway_segmentation import perform_lung_segmentation
from jobs.jobs_io import (
    get_input_directory_path_for_job,
    get_logger_for_job,
    get_result_file_path_for_job,
    get_temp_file_path_for_job,
)
from jobs.jobs_state import JobState, update_job_state

this_plid = os.path.basename(__file__).replace(".py", "")

# For this pipeline, take into account anything > 0 from the generated segmentation
hu_threshold = 0


def run(job_id: str, input_endpoint: str, medical_data: dict) -> None:
    logger = get_logger_for_job(job_id)
    update_job_state(job_id, JobState.STARTED.name, logger)

    update_job_state(job_id, JobState.FETCHING_INPUT.name, logger)
    dicom_directory_path = get_input_directory_path_for_job(job_id)
    fetch_and_unzip(input_endpoint, dicom_directory_path)

    update_job_state(job_id, JobState.READING_INPUT.name, logger)
    image_data_np_ndarray = read_dicom_as_np_ndarray_and_normalise(dicom_directory_path)

    update_job_state(job_id, JobState.PREPROCESSING.name, logger)
    # TODO no preprocessing step

    update_job_state(job_id, JobState.PERFORMING_SEGMENTATION.name, logger)
    segmented_lung, segmented_airway = perform_lung_segmentation(image_data_np_ndarray)

    update_job_state(job_id, JobState.POSTPROCESSING.name, logger)
    meshes = [
        generate_mesh(segmented_lung, hu_threshold),
        generate_mesh(segmented_airway, hu_threshold),
    ]

    obj_output_path = get_result_file_path_for_job(job_id)

    # TODO currently colours are hard coded for airway and lung
    colours = [[0, 0.3, 1.0, 0.2], [1.0, 1.0, 0.0, 1.0]]
    write_mesh_as_glb(meshes, obj_output_path, colours)

    update_job_state(job_id, JobState.DISPATCHING_OUTPUT.name, logger)
    dispatch_output(job_id, this_plid, medical_data)

    update_job_state(job_id, JobState.FINISHED.name, logger)


if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2], sys.argv[3])
