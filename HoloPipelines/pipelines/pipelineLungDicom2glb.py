from components import compCommonPath
from components import compJobStatus
from components import compDcm2nifti
from components.lungSegment.main import main as lungSegment
from components import compNifti2numpy
from components import compNumpy2obj
from components import compObj2glbWrapper
from components import compHttpRequest
from datetime import datetime
import pathlib
import sys
import logging


def main(job_id, dicom_path, output_glb_path, info_for_accessor):
    compJobStatus.updateStatus(job_id, "Pre-processing")
    generatedNiftiPath = compDcm2nifti.main(
        str(dicom_path),
        str(compCommonPath.nifti.joinpath(str(pathlib.PurePath(dicom_path).parts[-1]))),
    )  # convert dcm and move to temp path inside nifti folder. nifti will be in a sub folder named after the input dicom folder
    generatedSegmentedLungsNiftiPath = lungSegment(
        generatedNiftiPath, str(compCommonPath.nifti.joinpath("segmentedLungs"))
    )
    generatedNumpyList = compNifti2numpy.main(
        str(pathlib.Path(generatedSegmentedLungsNiftiPath).joinpath("lung.nii.gz"))
    )

    compJobStatus.updateStatus(job_id, "3D model generation")
    generatedObjPath = compNumpy2obj.main(
        generatedNumpyList,
        0.5,
        str(compCommonPath.obj.joinpath("nifti2glb_tempObj.obj")),
    )

    compJobStatus.updateStatus(job_id, "3D format conversion")
    generatedGlbPath = compObj2glbWrapper.main(
        generatedObjPath,
        str(pathlib.Path(output_glb_path)),
        delete_original_obj=True,
        compress_glb=False,
    )
    logging.info("lungDicom2glb: done, glb saved to {}".format(generatedGlbPath))
    compJobStatus.updateStatus(job_id, "Finished")
    compHttpRequest.sendFilePostRequestToAccessor(
        info_for_accessor["bodySite"] + "apply on lung segmentation",
        "http://localhost:3200/api/v1/holograms",
        info_for_accessor["description"],
        output_glb_path,
        info_for_accessor["bodySite"],
        info_for_accessor["dateOfImaging"],
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Generate glb mesh from dicom",
        info_for_accessor["author"],
        info_for_accessor["patient"],
    )


if __name__ == "__main__":
    main(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3], str(sys.argv[4])))
