from components import compJobStatus
from components import compCommonPath
from components import compDicom2numpy
from components import compNumpy2obj
from components import compObj2glbWrapper
from components import compPostToAccesor
from datetime import datetime
import pathlib
import json
import sys
import logging


def main(job_id, dicom_folder_path, output_glb_path, threshold, info_for_accessor):
    compJobStatus.updateStatus(job_id, "Pre-processing")
    generatedNumpyList = compDicom2numpy.main(str(pathlib.Path(dicom_folder_path)))

    compJobStatus.updateStatus(job_id, "3D model generation")
    generatedObjPath = compNumpy2obj.main(
        generatedNumpyList,
        threshold,
        str(
            compCommonPath.obj.joinpath(
                str(pathlib.PurePath(dicom_folder_path).parts[-1])
            )
        )
        + ".obj",
    )
    compJobStatus.updateStatus(job_id, "3D format conversion")
    generatedGlbPath = compObj2glbWrapper.main(
        generatedObjPath, output_glb_path, delete_original_obj=True, compress_glb=False
    )
    logging.info("dicom2glb: done, glb saved to {}".format(generatedGlbPath))
    compJobStatus.updateStatus(job_id, "Finished")
    infoForAccessor = json.loads(info_for_accessor)
    logging.info("Patient: " + json.dumps(infoForAccessor["patient"]))

    compPostToAccesor.sendFilePostRequestToAccessor(
        infoForAccessor["bodySite"] + "apply on generic bone segmentation",
        output_glb_path,
        infoForAccessor["description"],
        infoForAccessor["bodySite"],
        infoForAccessor["dateOfImaging"],
        datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "Generate glb mesh from dicom",
        infoForAccessor["author"],
        infoForAccessor["patient"],
    )


if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
