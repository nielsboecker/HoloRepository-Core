import pipelines.adapters.holostorage_accessor
from pipelines.components import compDicom2numpy
from pipelines.components import compNumpy2obj
from pipelines.wrappers.obj2gltf import convert_obj_to_glb
from pipelines.utils.job_status import JobStatus
from pipelines.utils.pipelines_info import get_pipeline_list
from pipelines.components.compJobStatus import update_status
from pipelines.tasks import receive_input
from pipelines.components import compJobPath
from pipelines.components import compJobStatus
from pipelines.tasks.dispatch_output import dispatch_output
import pathlib
import json
import sys
import logging

FORMAT = "%(asctime)-15s -function name:%(funcName)s -%(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)


def main(job_ID, dicom_download_url, meta_data):
    update_status(job_ID, JobStatus.FETCHING_DATA.name)
    dicom_folder_path = receive_input.fetch_and_unzip(job_ID, dicom_download_url)
    update_status(job_ID, JobStatus.PREPROCESSING.name)
    meta_data = json.loads(meta_data)
    generated_numpy_list = compDicom2numpy.main(str(pathlib.Path(dicom_folder_path)))
    threshold = 300

    update_status(job_ID, JobStatus.GENERATING_MODEL.name)
    generated_obj_path = compNumpy2obj.main(
        generated_numpy_list,
        threshold,
        compJobPath.make_str_job_path(job_ID, ["temp", "temp.obj"]),
    )
    update_status(job_ID, JobStatus.CONVERTING_MODEL.name)
    generated_glb_path = convert_obj_to_glb(
        generated_obj_path,
        compJobPath.make_str_job_path(job_ID, ["out", str(job_ID) + ".glb"]),
        delete_original_obj=True,
        compress_glb=False,
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
    compJobStatus.update_status(job_ID, "Cleaning up") # TODO: Enum
    compJobPath.clean_up(job_ID) # TODO: Enum
    update_status(job_ID, JobStatus.FINISHED.name)



if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
