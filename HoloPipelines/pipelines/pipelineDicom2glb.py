from pipelines.components import compJobStatus
from pipelines.components import compDicom2numpy
from pipelines.components import compNumpy2obj
from pipelines.components import compObj2glbWrapper
from pipelines.components import compPostToAccesor
from pipelines.components import compCombineInfoForAccesor
from pipelines.components import compFetchResource
from pipelines.components import compJobPath
from datetime import datetime
import pathlib
import json
import sys


def main(job_ID, dicom_download_url, info_for_accessor):
    compJobStatus.update_status(job_ID, "Fetching data")
    dicom_folder_path = compFetchResource.main(job_ID, dicom_download_url)
    compJobStatus.update_status(job_ID, "Pre-processing")
    info_for_accessor = json.loads(info_for_accessor)
    generated_numpy_list = compDicom2numpy.main(str(pathlib.Path(dicom_folder_path)))
    threshold = 300

    compJobStatus.update_status(job_ID, "3D model generation")
    generated_obj_path = compNumpy2obj.main(
        generated_numpy_list,
        threshold,
        compJobPath.make_str_job_path(job_ID, ["temp", "temp.obj"]),
    )
    compJobStatus.update_status(job_ID, "3D format conversion")
    generated_glb_path = compObj2glbWrapper.main(
        generated_obj_path,
        compJobPath.make_str_job_path(job_ID, ["out", str(job_ID) + ".glb"]),
        delete_original_obj=True,
        compress_glb=False,
    )
    print("dicom2glb: done, glb saved to {}".format(generated_glb_path))
    compJobStatus.update_status(job_ID, "Posting data")

    info_for_accessor = compCombineInfoForAccesor.add_info_for_accesor(
        info_for_accessor,
        "apply on generic bone segmentation",
        datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "Generate glb mesh from dicom",
        generated_glb_path,
    )
    print(json.dumps(info_for_accessor))
    print(datetime.now())
    compPostToAccesor.send_file_request_to_accessor(info_for_accessor)
    compJobStatus.update_status(job_ID, "Cleaning up")
    print(datetime.now())
    compJobPath.clean_up(job_ID)
    compJobStatus.update_status(job_ID, "Finished")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
