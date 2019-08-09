from components import compJobStatus
from components import compCommonPath
from components import compDicom2numpy
from components import compNumpy2obj
from components import compObj2glbWrapper
from components import compHttpRequest
from datetime import datetime
import pathlib
import sys


def main(jobID, dicomFolderPath, outputGlbPath, threshold,infoForAccessor):
    compJobStatus.updateStatus(jobID, "Pre-processing")
    generatedNumpyList = compDicom2numpy.main(str(pathlib.Path(dicomFolderPath)))

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
    compHttpRequest.sendFilePostRequestToAccessor(
        "http://localhost:3200",
        infoForAccessor["description"],
        outputGlbPath,infoForAccessor["bodySite"],
        infoForAccessor["dateOfImaging"],
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        infoForAccessor["author"],
        infoForAccessor["patient"]
        )
    

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4],sys.argv[5])
