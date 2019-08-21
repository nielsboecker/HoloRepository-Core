import sys

from config import MODEL_ABDOMINAL_SEGMENTATION_HOST, MODEL_ABDOMINAL_SEGMENTATION_PORT
from core.adapters.dicom_file import read_dicom_as_np_ndarray_and_normalise
from core.adapters.nifti_file import (
    convert_dicom_np_ndarray_to_nifti_image,
    read_nifti_as_np_array_and_normalise,
    write_nifti_image,
)
from core.clients import niftynet
from core.services.np_image_manipulation import downscale_and_conditionally_crop
from core.tasks.abdominal_organs_segmentation.split_to_separate_organs import (
    split_to_separate_organs,
)
from core.tasks.shared.receive_input import fetch_and_unzip
from jobs.jobs_io import (
    get_input_directory_path_for_job,
    get_logger_for_job,
    get_result_file_path_for_job,
    get_temp_file_path_for_job,
)
from jobs.jobs_state import JobState, update_job_state


def run(job_id: str, input_endpoint: str, medical_data: dict):
    logger = get_logger_for_job(job_id)
    update_job_state(job_id, JobState.STARTED.name, logger)

    update_job_state(job_id, JobState.FETCHING_INPUT.name, logger)
    dicom_directory_path = get_input_directory_path_for_job(job_id)
    fetch_and_unzip(input_endpoint, dicom_directory_path)

    update_job_state(job_id, JobState.READING_INPUT.name, logger)
    dicom_image_array = read_dicom_as_np_ndarray_and_normalise(dicom_directory_path)

    update_job_state(job_id, JobState.PREPROCESSING.name, logger)
    nifti_image = convert_dicom_np_ndarray_to_nifti_image(dicom_image_array)
    nifti_output_path = get_temp_file_path_for_job(job_id, "temp.nii")
    write_nifti_image(nifti_image, nifti_output_path)

    update_job_state(job_id, JobState.PERFORMING_SEGMENTATION.name, logger)
    segmented_output_file_path = get_temp_file_path_for_job(job_id, "segmented.nii")
    niftynet.call_model(
        MODEL_ABDOMINAL_SEGMENTATION_HOST,
        int(MODEL_ABDOMINAL_SEGMENTATION_PORT),
        nifti_output_path,
        segmented_output_file_path,
    )

    update_job_state(job_id, JobState.POSTPROCESSING.name, logger)
    segmented_array = read_nifti_as_np_array_and_normalise(segmented_output_file_path)
    segmented_array = downscale_and_conditionally_crop(segmented_array)
    split_to_separate_organs(segmented_array, get_result_file_path_for_job(job_id))

    # TODO: This expects 1 output instead of 8, and as outputs/out.glb
    # update_job_state(job_id, JobState.DISPATCHING_OUTPUT.name, logger)
    # dispatch_output(job_id, this_plid, medical_data)

    # update_job_state(job_id, JobState.FINISHED.name, logger)


if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2], sys.argv[3])
