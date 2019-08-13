from pipelines.components import compJobStatus
from pipelines.components import compCommonPath
from pipelines.components import compDicom2numpy
from pipelines.components import compNumpy2obj
from pipelines.components import compObj2glbWrapper
from pipelines.components import compPostToAccesor
from pipelines.components import compCombineInfoForAccesor
from datetime import datetime
import pathlib
import json
import sys


def main(jobID, dicomFolderPath, outputGlbPath, infoForAccessor):
    compJobStatus.updateStatus(jobID, "Pre-processing")
    generatedNumpyList = compDicom2numpy.main(str(pathlib.Path(dicomFolderPath)))
    threshold = 300

    compJobStatus.updateStatus(jobID, "3D model generation")
    generatedObjPath = compNumpy2obj.main(
        generatedNumpyList,
        threshold,
        str(
            compCommonPath.obj.joinpath(
                str(pathlib.PurePath(dicomFolderPath).parts[-1])
            )
        )
        + ".obj",
    )
    compJobStatus.updateStatus(jobID, "3D format conversion")
    generatedGlbPath = compObj2glbWrapper.main(
        generatedObjPath, outputGlbPath, deleteOriginalObj=True, compressGlb=False
    )
    print("dicom2glb: done, glb saved to {}".format(generatedGlbPath))
    compJobStatus.updateStatus(jobID, "Finished")

    infoForAccessor = compCombineInfoForAccesor.combineInfoForAccesor(
        infoForAccessor,
        "apply on generic bone segmentation",
        datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "Generate glb mesh from dicom",
        outputGlbPath,
    )
    print(json.dumps(infoForAccessor))
    compPostToAccesor.sendFilePostRequestToAccessor(infoForAccessor)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
