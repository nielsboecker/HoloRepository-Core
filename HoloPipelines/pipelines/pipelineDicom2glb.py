from components import compDicom2numpy
from components import compNumpy2obj
from pipelines.wrappers import obj2gltf
from components import compPostToAccesor
from components.compJobStatusEnum import JobStatus
from components import compCombineInfoForAccesor
from components.compGetPipelineListInfo import get_pipeline_list
from components.compJobStatus import update_status
from components import compFetchResource
from components import compJobPath
from components import compJobStatus
import pathlib
import json
import sys
import logging

FORMAT = "%(asctime)-15s -function name:%(funcName)s -%(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)


def main(job_ID, dicom_download_url, meta_data):
    update_status(job_ID, JobStatus.FETCHINGDATA.name)
    dicom_folder_path = compFetchResource.main(job_ID, dicom_download_url)
    update_status(job_ID, JobStatus.PPREPROCESSING.name)
    meta_data = json.loads(meta_data)
    generated_numpy_list = compDicom2numpy.main(str(pathlib.Path(dicom_folder_path)))
    threshold = 300

    update_status(job_ID, JobStatus.MODELGENERATION.name)
    generated_obj_path = compNumpy2obj.main(
        generated_numpy_list,
        threshold,
        compJobPath.make_str_job_path(job_ID, ["temp", "temp.obj"]),
    )
    update_status(job_ID, JobStatus.MODELCONVERSION.name)
    generated_glb_path = obj2gltf.main(
        generated_obj_path,
        compJobPath.make_str_job_path(job_ID, ["out", str(job_ID) + ".glb"]),
        delete_original_obj=True,
        compress_glb=False,
    )

    list_of_pipeline = get_pipeline_list()
    logging.debug("dicom2glb: done, glb saved to {}".format(generated_glb_path))
    meta_data = compCombineInfoForAccesor.add_info_for_accesor(
        meta_data,
        "apply on generic bone segmentation",
        "Generate with " + list(list_of_pipeline.keys())[1] + " pipeline",
        generated_glb_path,
    )
    logging.debug("meta_data: " + json.dumps(meta_data))
    compPostToAccesor.send_file_request_to_accessor(meta_data)
    compJobStatus.update_status(job_ID, "Cleaning up") # TODO: Enum
    compJobPath.clean_up(job_ID) # TODO: Enum
    update_status(job_ID, JobStatus.FINISHED.name)



if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
