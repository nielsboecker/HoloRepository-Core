from pipelines.components import compCommonPath
from pipelines.components import compJobStatus
from pipelines.components import compNifti2numpy
from pipelines.components import compNumpy2obj
from pipelines.components import compObj2glbWrapper
from pipelines.components import compHttpRequest
import pathlib
import sys
import logging
from datetime import datetime


def main(job_id, input_nifti_path, output_glb_path, threshold, info_for_accessor):
    compJobStatus.update_status(job_id, "Pre-processing")
    generatedNumpyList = compNifti2numpy.main(str(pathlib.Path(input_nifti_path)))

    compJobStatus.update_status(job_id, "3D model generation")
    generatedObjPath = compNumpy2obj.main(
        generatedNumpyList,
        threshold,
        str(compCommonPath.obj.joinpath("nifti2glb_tempObj.obj")),
    )

    compJobStatus.update_status(job_id, "3D format conversion")
    generatedGlbPath = compObj2glbWrapper.main(
        generatedObjPath,
        str(pathlib.Path(output_glb_path)),
        delete_original_obj=True,
        compress_glb=False,
    )
    logging.info("nifti2glb: done, glb saved to {}".format(generatedGlbPath))
    compJobStatus.update_status(job_id, "Finished")
    compHttpRequest.send_file_post_request(
        info_for_accessor["bodySite"] + "apply on generic bone segmentation",
        "http://localhost:3200/api/v1/holograms",
        info_for_accessor["description"],
        output_glb_path,
        info_for_accessor["bodySite"],
        info_for_accessor["dateOfImaging"],
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Generate glb mesh from nifti",
        info_for_accessor["author"],
        info_for_accessor["patient"],
    )


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
