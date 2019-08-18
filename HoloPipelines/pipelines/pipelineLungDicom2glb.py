# TODO: Don't understand Pap's comments here. Dev is already merged back into this?!

# from pipelines.components import (
#     compCommonPath,
# )  # needs to be removed when compDcm2nifti is replaced (please see other comments below)
import pipelines.adapters.holostorage_accessor
import pipelines.services.format_conversion
import pipelines.state.job_status
from pipelines.adapters.nifti_file import read_nifti_as_np_array_and_normalise
from pipelines.config.io_paths import nifti_path
from pipelines.services.format_conversion import convert_numpy_to_obj, convert_dicom_to_nifti, convert_obj_to_glb
import pipelines.components.lungSegment.main as comp_lung_segment
from pipelines.tasks.shared.dispatch_output import dispatch_output
from pipelines.tasks.shared import receive_input
from pipelines.components import compJobPath
from pipelines.utils.job_status import JobStatus
from pipelines.utils.pipelines_info import get_pipeline_list

import pathlib
import sys
import logging

logging.basicConfig(level=logging.INFO)


def main(job_ID, dicom_download_url, meta_data):
    pipelines.state.job_status.post_status_update(job_ID, "Fetching data")
    dicom_path = receive_input.fetch_and_unzip(job_ID, dicom_download_url)
    pipelines.state.job_status.post_status_update(job_ID, JobStatus.PREPROCESSING.name)
    generated_nifti_path = convert_dicom_to_nifti(  # compDcm2nifti here is outdated (still has GDCM dependency, will need to be merged with dev). comp should also be updated to return the full path to nii file, not its folder
        str(dicom_path),
        str(
            nifti_path.joinpath(str(pathlib.PurePath(dicom_path).parts[-1]))
        ),  # this will need to be updated once compDcm2nifti is replaced
    )  # this comment will be outdated when changes from lines above happens >>> convert dcm and move to temp path inside nifti folder. nifti will be in a sub folder named after the input dicom folder
    generated_segmented_lung_nifti_path = comp_lung_segment(
        generated_nifti_path,
        compJobPath.make_str_job_path(job_ID, ["temp"], create_sub_directories=False),
    )
    generated_numpy_list = read_nifti_as_np_array_and_normalise(generated_segmented_lung_nifti_path)

    pipelines.state.job_status.post_status_update(job_ID, JobStatus.GENERATING_MODEL.name)

    generated_obj_path = convert_numpy_to_obj(
        generated_numpy_list,
        0.5,
        compJobPath.make_str_job_path(job_ID, ["temp", "temp.obj"]),
    )

    pipelines.state.job_status.post_status_update(job_ID, JobStatus.CONVERTING_MODEL.name)

    generated_glb_path = convert_obj_to_glb(
        generated_obj_path,
        compJobPath.make_str_job_path(job_ID, ["out", str(job_ID) + ".glb"]),
        delete_original_obj=True,
        compress_glb=False,
    )
    logging.debug("lungDicom2glb: done, glb saved to {}".format(generated_glb_path))

    pipelines.state.job_status.post_status_update(job_ID, "Posting data")
    list_of_pipeline = get_pipeline_list()
    meta_data = pipelines.adapters.holostorage_accessor.add_info_for_accesor(
        meta_data,
        "apply on generic bone segmentation",
        "Generate with " + list(list_of_pipeline.keys())[1] + " pipeline",
        generated_glb_path,
    )

    # TODO: Verify if this works after merge...
    dispatch_output(meta_data)

    pipelines.state.job_status.post_status_update(job_ID, "Cleaning up")
    compJobPath.clean_up(job_ID)
    pipelines.state.job_status.post_status_update(job_ID, JobStatus.FINISHED.name)
