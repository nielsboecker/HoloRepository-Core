"""
This pipeline performs automatic segmentation of lungs. It uses an existing algorithmic
implementation for the actual segmentation.

Algorithm: https://github.com/wanwanbeen/ct_lung_segmentation
Paper: Discriminative Localization in CNNs for Weakly-Supervised Segmentation of Pulmonary Nodules
Xinyang Feng, Jie Yang, Andrew F. Laine, Elsa D. Angelini
"""

import os

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

    nifti_image_as_np_array5 = read_nifti_as_np_array(
        "./cortical_gray_matter_seg.nii", normalise=True
    )

    nifti_image_as_np_array1 = read_nifti_as_np_array(
        "./white_matter_lesions_seg.nii", normalise=True
    )


    obj_output_path = get_result_file_path_for_job(job_id)
    segment = []

    segment.append(generate_mesh(nifti_image_as_np_array5, hu_threshold))
    segment.append(generate_mesh(nifti_image_as_np_array1, hu_threshold))

    write_mesh_as_glb(segment, obj_output_path,[[0,0.3,1.0,0.2],[1.0,1.0,0.0,1.0]],{
    1: "cortical_gray_matter",
    2: "basal_ganglia",
})

    update_job_state(job_id, JobState.DISPATCHING_OUTPUT.name, logger)
    dispatch_output(job_id, this_plid, medical_data)

    update_job_state(job_id, JobState.FINISHED.name, logger)
