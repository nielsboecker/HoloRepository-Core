import json
import logging
import pathlib
import sys

import numpy as np

import core.adapters.glb_file
import core.clients.holostorage_accessor
import jobs.job_status
from core.adapters.dicom_file import read_dicom_as_np_ndarray_and_normalise
from core.adapters.glb_file import convert_obj_to_glb_and_write
from core.adapters.obj_file import write_mesh_as_obj
from core.services.marching_cubes import generate_mesh
from core.tasks.shared import receive_input
from core.tasks.shared.dispatch_output import dispatch_output
from core.utils.pipelines_info import get_pipeline_list
from jobs import job_controller
from jobs.job_status import post_status_update, JobStatus


def main(job_ID, dicom_download_url, meta_data):
    post_status_update(job_ID, JobStatus.FETCHING_DATA.name)
    dicom_folder_path = receive_input.fetch_and_unzip(job_ID, dicom_download_url)
    post_status_update(job_ID, JobStatus.PREPROCESSING.name)
    meta_data = json.loads(meta_data)
    dicom_image: np.ndarray = read_dicom_as_np_ndarray_and_normalise(
        str(pathlib.Path(dicom_folder_path))
    )
    threshold = 300

    post_status_update(job_ID, JobStatus.GENERATING_MODEL.name)

    obj_output_path = job_controller.make_str_job_path(job_ID, ["temp", "temp.obj"])
    verts, faces, norm = generate_mesh(dicom_image, threshold)
    write_mesh_as_obj(verts, faces, norm, obj_output_path)

    post_status_update(job_ID, JobStatus.CONVERTING_MODEL.name)
    generated_glb_path = convert_obj_to_glb_and_write(
        obj_output_path,
        job_controller.make_str_job_path(job_ID, ["out", str(job_ID) + ".glb"]),
    )

    list_of_pipeline = get_pipeline_list()
    logging.debug("dicom2glb: done, glb saved to {}".format(generated_glb_path))
    meta_data = core.clients.holostorage_accessor.add_info_for_accesor(
        meta_data,
        "apply on generic bone segmentation",
        "Generate with " + list(list_of_pipeline.keys())[1] + " pipeline",
        generated_glb_path,
    )
    logging.debug("meta_data: " + json.dumps(meta_data))
    dispatch_output(meta_data)
    jobs.job_status.post_status_update(job_ID, "Cleaning up")  # TODO: Enum
    job_controller.clean_up(job_ID)  # TODO: Enum
    post_status_update(job_ID, JobStatus.FINISHED.name)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
