from components import compCommonPath
from components import compJobStatus
from components import compDcm2nifti
from components.lungSegment.main import main as lungSegment
from components import compNifti2numpy
from components import compNumpy2obj
from components import compObj2glbWrapper
from components import compPostToAccesor
from datetime import datetime
import pathlib
import sys
import json


def main(jobID, dicomPath, outputGlbPath, infoForAccessor):
    compJobStatus.update_status(jobID, "Pre-processing")
    generatedNiftiPath = compDcm2nifti.main(
        str(dicomPath),
        str(compCommonPath.nifti.joinpath(str(pathlib.PurePath(dicomPath).parts[-1]))),
    )  # convert dcm and move to temp path inside nifti folder. nifti will be in a sub folder named after the input dicom folder
    generatedSegmentedLungsNiftiPath = lungSegment(
        generatedNiftiPath, str(compCommonPath.nifti.joinpath("segmentedLungs"))
    )
    generatedNumpyList = compNifti2numpy.main(
        str(pathlib.Path(generatedSegmentedLungsNiftiPath).joinpath("lung.nii.gz"))
    )

    compJobStatus.update_status(jobID, "3D model generation")
    generatedObjPath = compNumpy2obj.main(
        generatedNumpyList,
        0.5,
        str(compCommonPath.obj.joinpath("nifti2glb_tempObj.obj")),
    )

    compJobStatus.update_status(jobID, "3D format conversion")
    generatedGlbPath = compObj2glbWrapper.main(
        generatedObjPath,
        str(pathlib.Path(outputGlbPath)),
        deleteOriginalObj=True,
        compressGlb=False,
    )
    print("lungDicom2glb: done, glb saved to {}".format(generatedGlbPath))
    compJobStatus.update_status(jobID, "Finished")
    infoForAccessor = json.loads(infoForAccessor)
    compPostToAccesor.sendFilePostRequestToAccessor(
        infoForAccessor["bodySite"] + "apply on generic bone segmentation",
        outputGlbPath,
        infoForAccessor["description"],
        infoForAccessor["bodySite"],
        infoForAccessor["dateOfImaging"],
        datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "Generate glb mesh from dicom",
        infoForAccessor["author"],
        infoForAccessor["patient"],
    )


if __name__ == "__main__":
    main(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3], str(sys.argv[4])))
