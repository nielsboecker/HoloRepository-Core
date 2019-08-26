from components import (
    compCommonPath,
)  # needs to be removed when compDcm2nifti is replaced (please see other comments below)
from components import compJobStatus
from components import compDicom2nifti
import components.lungSegment.main as comp_lung_segment
from components import compNifti2numpy
from components import compNumpy2obj
from components import compObj2glbWrapper
from components import compPostToAccesor
from components import compFetchResource
from components import compJobPath
from components.compJobStatusEnum import JobStatus
from components import compCombineInfoForAccesor
from components.compGetPipelineListInfo import get_pipeline_list

import pathlib
import sys
import logging

logging.basicConfig(level=logging.INFO)


def main(job_ID, dicom_download_url, meta_data):
    compJobStatus.update_status(job_ID, "Fetching data")
    dicom_path = compFetchResource.main(job_ID, dicom_download_url)
    compJobStatus.update_status(job_ID, JobStatus.PPREPROCESSING.name)
    generated_nifti_path = compDicom2nifti.main(  # compDcm2nifti here is outdated (still has GDCM dependency, will need to be merged with dev). comp should also be updated to return the full path to nii file, not its folder
        str(dicom_path),
        str(
            compCommonPath.nifti.joinpath(str(pathlib.PurePath(dicom_path).parts[-1]))
        ),  # this will need to be updated once compDcm2nifti is replaced
    )  # this comment will be outdated when changes from lines above happens >>> convert dcm and move to temp path inside nifti folder. nifti will be in a sub folder named after the input dicom folder
    generated_segmented_lung_nifti_path = comp_lung_segment(
        generated_nifti_path,
        compJobPath.make_str_job_path(job_ID, ["temp"], create_sub_directories=False),
    )
    generated_numpy_list = compNifti2numpy.main(generated_segmented_lung_nifti_path)

    compJobStatus.update_status(job_ID, JobStatus.MODELGENERATION.name)

    generated_obj_path = compNumpy2obj.main(
        generated_numpy_list,
        0.5,
        compJobPath.make_str_job_path(job_ID, ["temp", "temp.obj"]),
    )

    compJobStatus.update_status(job_ID, JobStatus.MODELCONVERSION.name)

    generated_glb_path = compObj2glbWrapper.main(
        generated_obj_path,
        compJobPath.make_str_job_path(job_ID, ["out", str(job_ID) + ".glb"]),
        delete_original_obj=True,
        compress_glb=False,
    )
    logging.debug("lungDicom2glb: done, glb saved to {}".format(generated_glb_path))

    compJobStatus.update_status(job_ID, "Posting data")
    list_of_pipeline = get_pipeline_list()
    meta_data = compCombineInfoForAccesor.add_info_for_accesor(
        meta_data,
        "apply on generic bone segmentation",
        "Generate with " + list(list_of_pipeline.keys())[1] + " pipeline",
        generated_glb_path,
    )

    # TODO: Verify if this works after merge...
    compPostToAccesor.send_file_request_to_accessor(meta_data)

    compJobStatus.update_status(job_ID, "Cleaning up")
    compJobPath.clean_up(job_ID)
    compJobStatus.update_status(job_ID, JobStatus.FINISHED.name)


if __name__ == "__main__":
    main(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]))
