from pipelines.components import (
    compCommonPath,
)  # needs to be removed when compDcm2nifti is replaced (please see other comments below)
from pipelines.components import compJobStatus
from pipelines.components import compDcm2nifti
from pipelines.components.lungSegment.main import main as lungSegment
from pipelines.components import compNifti2numpy
from pipelines.components import compNumpy2obj
from pipelines.components import compObj2glbWrapper
from pipelines.components import compPostToAccesor
from pipelines.components import compFetchResource
from pipelines.components import compJobPath
from datetime import datetime
import pathlib
import sys
import json


def main(job_ID, dicom_download_url, info_for_accessor):
    compJobStatus.update_status(job_ID, "Fetching data")
    dicom_path = compFetchResource.main(job_ID, dicom_download_url)
    compJobStatus.update_status(job_ID, "Pre-processing")
    generated_nifti_path = compDcm2nifti.main(  # compDcm2nifti here is outdated (still has GDCM dependency, will need to be merged with dev). comp should also be updated to return the full path to nii file, not its folder
        str(dicom_path),
        str(
            compCommonPath.nifti.joinpath(str(pathlib.PurePath(dicom_path).parts[-1]))
        ),  # this will need to be updated once compDcm2nifti is replaced
    )  # this comment will be outdated when changes from lines above happens >>> convert dcm and move to temp path inside nifti folder. nifti will be in a sub folder named after the input dicom folder
    generated_segmented_lung_nifti_path = lungSegment(
        generated_nifti_path,
        compJobPath.make_str_job_path(job_ID, ["temp"], create_sub_directories=False),
    )
    generated_numpy_list = compNifti2numpy.main(generated_segmented_lung_nifti_path)

    compJobStatus.update_status(job_ID, "3D model generation")
    generated_obj_path = compNumpy2obj.main(
        generated_numpy_list,
        0.5,
        compJobPath.make_str_job_path(job_ID, ["temp", "temp.obj"]),
    )

    compJobStatus.update_status(job_ID, "3D format conversion")
    generated_glb_path = compObj2glbWrapper.main(
        generated_obj_path,
        compJobPath.make_str_job_path(job_ID, ["out", str(job_ID) + ".glb"]),
        delete_original_obj=True,
        compress_glb=False,
    )
    print("lungDicom2glb: done, glb saved to {}".format(generated_glb_path))
    compJobStatus.update_status(job_ID, "Posting data")
    info_for_accessor = json.loads(info_for_accessor)
    compPostToAccesor.send_file_request_to_accessor(
        info_for_accessor["bodySite"] + "apply on generic bone segmentation",
        generated_glb_path,
        info_for_accessor["description"],
        info_for_accessor["bodySite"],
        info_for_accessor["dateOfImaging"],
        datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "Generate glb mesh from dicom",
        info_for_accessor["author"],
        info_for_accessor["patient"],
    )
    compJobStatus.update_status(job_ID, "Cleaning up")
    compJobPath.clean_up(job_ID)
    compJobStatus.update_status(job_ID, "Finished")


if __name__ == "__main__":
    main(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]))
