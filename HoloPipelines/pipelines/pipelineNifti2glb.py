# pipeline left in current state (work with local files) as unsure if there's a use case where user can download nii from PACS
# could be left as is for internal use? Keep this file but delete index from pipelineList.json?

# do i need status update on this 'internal' pipeline?
import pipelines.adapters.holostorage_accessor
import pipelines.state.job_status
from pipelines.components import compNifti2numpy
from pipelines.components import compNumpy2obj
from pipelines.wrappers.obj2gltf import convert_obj_to_glb
from pipelines.tasks.dispatch_output import dispatch_output
from pipelines.components import compJobPath
from pipelines.utils.job_status import JobStatus
from pipelines.utils.pipelines_info import get_pipeline_list
import pathlib
import json
import sys
import logging

FORMAT = "%(asctime)-15s -function name:%(funcName)s -%(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)


def main(job_ID, input_nifti_path, output_glb_path, threshold, meta_data):
    pipelines.state.job_status.post_status_update(job_ID, JobStatus.PREPROCESSING.name)
    generated_numpy_list = compNifti2numpy.main(str(pathlib.Path(input_nifti_path)))

    logging.debug("job start: " + json.dumps(meta_data))

    pipelines.state.job_status.post_status_update(job_ID, JobStatus.GENERATING_MODEL.name)
    generated_obj_path = compNumpy2obj.main(
        generated_numpy_list,
        threshold,
        compJobPath.make_str_job_path(job_ID, ["temp", "temp.obj"]),
    )

    pipelines.state.job_status.post_status_update(job_ID, JobStatus.CONVERTING_MODEL.name)
    generated_glb_path = convert_obj_to_glb(
        generated_obj_path,
        str(pathlib.Path(output_glb_path)),
        delete_original_obj=True,
        compress_glb=False,
    )
    logging.info("nifti2glb: done, glb saved to {}".format(generated_glb_path))
    print("nifti2glb: done, glb saved to {}".format(generated_glb_path))

    list_of_pipeline = get_pipeline_list()
    meta_data = pipelines.adapters.holostorage_accessor.add_info_for_accesor(
        meta_data,
        "apply on generic bone segmentation",
        "Generate with " + list(list_of_pipeline.keys())[1] + " pipeline",
        output_glb_path,
    )
    # TODO: Verify this works after merge
    pipelines.state.job_status.post_status_update(job_ID, "Posting data")
    dispatch_output(meta_data)

    pipelines.state.job_status.post_status_update(job_ID, "Cleaning up")
    compJobPath.clean_up(job_ID)
    pipelines.state.job_status.post_status_update(job_ID, JobStatus.FINISHED.name)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
