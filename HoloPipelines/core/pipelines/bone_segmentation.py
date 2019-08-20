import json
import pathlib
import sys

import numpy as np

import core.adapters.glb_file
import core.clients.holostorage_accessor
import jobs.job_status
import jobs.jobs_io
from core.adapters.dicom_file import read_dicom_as_np_ndarray_and_normalise
from core.adapters.glb_file import convert_obj_to_glb_and_write
from core.adapters.obj_file import write_mesh_as_obj
from core.services.marching_cubes import generate_mesh
from core.services.np_image_manipulation import downscale_and_conditionally_crop
from core.tasks.shared import receive_input
from core.tasks.shared.dispatch_output import dispatch_output
from jobs.job_status import JobStatus, post_status_update
from jobs.jobs_io import get_logger_for_job, get_temp_file_path_for_job


def main(job_id: str, input_endpoint: str, medical_data: dict):
    logger = get_logger_for_job(job_id)

    post_status_update(job_id, JobStatus.FETCHING_DATA.name)
    dicom_folder_path = receive_input.fetch_and_unzip(job_id, input_endpoint)
    post_status_update(job_id, JobStatus.PREPROCESSING.name)
    logger.info("dicom to numpy")
    dicom_image: np.ndarray = read_dicom_as_np_ndarray_and_normalise(
        str(pathlib.Path(dicom_folder_path))
    )

    downscaled_image = downscale_and_conditionally_crop(dicom_image)

    post_status_update(job_id, JobStatus.GENERATING_MODEL.name)
    obj_output_path = get_temp_file_path_for_job(job_id, "temp.obj")
    threshold = 300
    verts, faces, norm = generate_mesh(downscaled_image, threshold)
    write_mesh_as_obj(verts, faces, norm, obj_output_path)

    post_status_update(job_id, JobStatus.CONVERTING_MODEL.name)
    generated_glb_path = convert_obj_to_glb_and_write(
        obj_output_path, get_temp_file_path_for_job(job_id, "out.glb")
    )

    logger.info("dicom2glb: done, glb saved to {}".format(generated_glb_path))
    medical_data = core.clients.holostorage_accessor.add_info_for_accesor(
        medical_data,
        "apply on generic bone segmentation",
        "Generated with bone_segmentation pipeline",
        generated_glb_path,
    )
    logger.info("meta_data: " + json.dumps(medical_data))
    logger.info("send")
    dispatch_output(medical_data)
    jobs.job_status.post_status_update(job_id, "Cleaning up")  # TODO: Enum
    # job_controller.clean_up(job_id)  # TODO: Enum
    post_status_update(job_id, JobStatus.FINISHED.name)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
