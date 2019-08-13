from components import compCommonPath
from components import compJobStatus
from components import compNifti2numpy
from components import compNumpy2obj
from components import compObj2glbWrapper
from components import compPostToAccesor
import pathlib
import sys
from datetime import datetime
import json


def main(jobID, inputNiftiPath, outputGlbPath, threshold, infoForAccessor):
    compJobStatus.updateStatus(jobID, "Pre-processing")
    generatedNumpyList = compNifti2numpy.main(str(pathlib.Path(inputNiftiPath)))

    compJobStatus.updateStatus(jobID, "3D model generation")
    generatedObjPath = compNumpy2obj.main(
        generatedNumpyList,
        threshold,
        str(compCommonPath.obj.joinpath("nifti2glb_tempObj.obj")),
    )

    compJobStatus.updateStatus(jobID, "3D format conversion")
    generatedGlbPath = compObj2glbWrapper.main(
        generatedObjPath,
        str(pathlib.Path(outputGlbPath)),
        deleteOriginalObj=True,
        compressGlb=False,
    )
    print("nifti2glb: done, glb saved to {}".format(generatedGlbPath))
    compJobStatus.updateStatus(jobID, "Finished")
    infoForAccessor = json.loads(infoForAccessor)
    compPostToAccesor.sendFilePostRequestToAccessor(
        infoForAccessor["bodySite"] + "apply on generic bone segmentation",
        outputGlbPath,
        infoForAccessor["description"],
        infoForAccessor["bodySite"],
        infoForAccessor["dateOfImaging"],
        datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "Generate glb mesh from nifti",
        infoForAccessor["author"],
        infoForAccessor["patient"],
    )


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
