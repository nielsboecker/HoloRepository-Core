# TODO: Don't understand Pap's comments here. Dev is already merged back into this?!

# from pipelines.components import (
#     compCommonPath,
# )  # needs to be removed when compDcm2nifti is replaced (please see other comments below)
import pipelines.clients.holostorage_accessor
import pipelines.adapters.glb_file
import pipelines.state.job_status
from pipelines.adapters.dicom_file import read_dicom_as_np_ndarray_and_normalise
from pipelines.adapters.nifti_file import read_nifti_as_np_array_and_normalise, write_nifti_image
from pipelines.adapters.obj_file import write_mesh_as_obj
from pipelines.config.io_paths import nifti_path
from pipelines.adapters.glb_file import convert_obj_to_glb_and_write
from pipelines.services.marching_cubes import generate_mesh
from pipelines.tasks.shared.dispatch_output import dispatch_output
from pipelines.tasks.shared import receive_input
from pipelines.components import compJobPath
from pipelines.utils.job_status import JobStatus
from pipelines.utils.pipelines_info import get_pipeline_list
from pipelines.adapters.nifti_file import convert_dicom_np_ndarray_to_nifti_image

import pathlib
import logging

from pipelines.wrappers.lung_and_airway_segmentation import perform_lung_segmentation


def main(job_ID, dicom_download_url, meta_data):
    pipelines.state.job_status.post_status_update(job_ID, "Fetching data")
    dicom_path = receive_input.fetch_and_unzip(job_ID, dicom_download_url)
    pipelines.state.job_status.post_status_update(job_ID, JobStatus.PREPROCESSING.name)

    dicom_image_array = read_dicom_as_np_ndarray_and_normalise(dicom_path)
    nifti_image = convert_dicom_np_ndarray_to_nifti_image(dicom_image_array)

    nifti_output_path = str(nifti_path.joinpath(str(pathlib.PurePath(dicom_path).parts[-1])))
    write_nifti_image(nifti_image, nifti_output_path)

    generated_segmented_lung_nifti_path = perform_lung_segmentation(
        nifti_output_path,
        compJobPath.make_str_job_path(job_ID, ["temp"], create_sub_directories=False),
    )
    nifti_image_as_np_array = read_nifti_as_np_array_and_normalise(generated_segmented_lung_nifti_path)

    pipelines.state.job_status.post_status_update(job_ID, JobStatus.GENERATING_MODEL.name)
    obj_output_path = compJobPath.make_str_job_path(job_ID, ["temp", "temp.obj"])
    threshold = 0.5
    verts, faces, norm = generate_mesh(nifti_image_as_np_array, threshold)
    write_mesh_as_obj(verts, faces, norm, obj_output_path)

    pipelines.state.job_status.post_status_update(job_ID, JobStatus.CONVERTING_MODEL.name)
    generated_glb_path = convert_obj_to_glb_and_write(
        obj_output_path,
        compJobPath.make_str_job_path(job_ID, ["out", str(job_ID) + ".glb"]),
    )
    logging.debug("lungDicom2glb: done, glb saved to {}".format(generated_glb_path))

    pipelines.state.job_status.post_status_update(job_ID, "Posting data")
    list_of_pipeline = get_pipeline_list()
    meta_data = pipelines.clients.holostorage_accessor.add_info_for_accesor(
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
