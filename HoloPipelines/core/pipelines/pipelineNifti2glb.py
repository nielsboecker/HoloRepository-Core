# pipeline left in current state (work with local files) as unsure if there's a use case where user can download nii from PACS
# could be left as is for internal use? Keep this file but delete index from pipelines_list.json?

import json
import logging
import pathlib

import core.adapters.glb_file

# do i need status update on this 'internal' pipeline?
import core.clients.holostorage_accessor
import jobs.job_status
from core.adapters.glb_file import convert_obj_to_glb_and_write
from core.adapters.nifti_file import read_nifti_as_np_array_and_normalise
from core.adapters.obj_file import write_mesh_as_obj
from core.services.marching_cubes import generate_mesh
from core.tasks.shared.dispatch_output import dispatch_output
from core.utils.job_status import JobStatus
from core.utils.pipelines_info import get_pipeline_list
from jobs import job_controller


def main(job_ID, input_nifti_path, output_glb_path, threshold, meta_data):
    jobs.job_status.post_status_update(job_ID, JobStatus.PREPROCESSING.name)
    nifti_image_as_np_array = read_nifti_as_np_array_and_normalise(
        str(pathlib.Path(input_nifti_path))
    )

    logging.debug("job start: " + json.dumps(meta_data))

    jobs.job_status.post_status_update(job_ID, JobStatus.GENERATING_MODEL.name)
    obj_output_path = job_controller.make_str_job_path(job_ID, ["temp", "temp.obj"])
    verts, faces, norm = generate_mesh(nifti_image_as_np_array, threshold)
    write_mesh_as_obj(verts, faces, norm, obj_output_path)

    jobs.job_status.post_status_update(job_ID, JobStatus.CONVERTING_MODEL.name)
    generated_glb_path = convert_obj_to_glb_and_write(
        obj_output_path, str(pathlib.Path(output_glb_path))
    )
    logging.info("nifti2glb: done, glb saved to {}".format(generated_glb_path))
    print("nifti2glb: done, glb saved to {}".format(generated_glb_path))

    list_of_pipeline = get_pipeline_list()
    meta_data = core.clients.holostorage_accessor.add_info_for_accesor(
        meta_data,
        "apply on generic bone segmentation",
        "Generate with " + list(list_of_pipeline.keys())[1] + " pipeline",
        output_glb_path,
    )
    # TODO: Verify this works after merge
    jobs.job_status.post_status_update(job_ID, "Posting data")
    dispatch_output(meta_data)

    jobs.job_status.post_status_update(job_ID, "Cleaning up")
    job_controller.clean_up(job_ID)
    jobs.job_status.post_status_update(job_ID, JobStatus.FINISHED.name)
