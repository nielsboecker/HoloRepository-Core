import pipelines.adapters.holostorage_accessor
import pipelines.adapters.glb_file
import pipelines.state.job_status
from pipelines.adapters.dicom_file import read_dicom_as_np_ndarray_and_normalise
from pipelines.adapters.obj_file import write_mesh_as_obj
from pipelines.adapters.glb_file import convert_obj_to_glb
from pipelines.services.marching_cubes import generate_mesh
from pipelines.utils.job_status import JobStatus
from pipelines.utils.pipelines_info import get_pipeline_list
from pipelines.state.job_status import post_status_update
from pipelines.tasks.shared import receive_input
from pipelines.components import compJobPath
from pipelines.tasks.shared.dispatch_output import dispatch_output
import pathlib
import json
import sys
import logging
import numpy as np

FORMAT = "%(asctime)-15s -function name:%(funcName)s -%(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)


def main(job_ID, dicom_download_url, meta_data):
    post_status_update(job_ID, JobStatus.FETCHING_DATA.name)
    dicom_folder_path = receive_input.fetch_and_unzip(job_ID, dicom_download_url)
    post_status_update(job_ID, JobStatus.PREPROCESSING.name)
    meta_data = json.loads(meta_data)
    dicom_image: np.ndarray = read_dicom_as_np_ndarray_and_normalise(str(pathlib.Path(dicom_folder_path)))
    threshold = 300

    post_status_update(job_ID, JobStatus.GENERATING_MODEL.name)

    obj_output_path = compJobPath.make_str_job_path(job_ID, ["temp", "temp.obj"])
    verts, faces, norm = generate_mesh(dicom_image, threshold)
    write_mesh_as_obj(verts, faces, norm, obj_output_path)

    post_status_update(job_ID, JobStatus.CONVERTING_MODEL.name)
    generated_glb_path = convert_obj_to_glb(
        obj_output_path,
        compJobPath.make_str_job_path(job_ID, ["out", str(job_ID) + ".glb"]),
    )

    list_of_pipeline = get_pipeline_list()
    logging.debug("dicom2glb: done, glb saved to {}".format(generated_glb_path))
    meta_data = pipelines.adapters.holostorage_accessor.add_info_for_accesor(
        meta_data,
        "apply on generic bone segmentation",
        "Generate with " + list(list_of_pipeline.keys())[1] + " pipeline",
        generated_glb_path,
    )
    logging.debug("meta_data: " + json.dumps(meta_data))
    dispatch_output(meta_data)
    pipelines.state.job_status.post_status_update(job_ID, "Cleaning up") # TODO: Enum
    compJobPath.clean_up(job_ID) # TODO: Enum
    post_status_update(job_ID, JobStatus.FINISHED.name)



if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
