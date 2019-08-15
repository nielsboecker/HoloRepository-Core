from pipelines.components import compJobStatus
from pipelines.components import compCommonPath
from pipelines.components import compDicom2numpy
from pipelines.components import compNumpy2obj
from pipelines.components import compObj2glbWrapper
from pipelines.components import compPostToAccesor
from pipelines.components import compCombineInfoForAccesor
from pipelines.components import compFetchResource
from pipelines.components import compJobCleanup
from datetime import datetime
import pathlib
import json
import sys


def main(jobID, dicomDownloadUrl, infoForAccessor):
    compJobStatus.update_status(jobID, "Fetching data")
    dicomFolderPath = compFetchResource.main(jobID, dicomDownloadUrl)
    compJobStatus.update_status(jobID, "Pre-processing")
    generatedNumpyList = compDicom2numpy.main(str(pathlib.Path(dicomFolderPath)))
    threshold = 300

    compJobStatus.update_status(jobID, "3D model generation")
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
    compJobStatus.update_status(jobID, "3D format conversion")
    generatedGlbPath = compObj2glbWrapper.main(
        generatedObjPath,
        str(pathlib.Path(dicomFolderPath).parent.joinpath(str(jobID) + ".glb")),
        deleteOriginalObj=True,
        compressGlb=False,
    )
    print("dicom2glb: done, glb saved to {}".format(generatedGlbPath))
    compJobStatus.update_status(jobID, "Posting data")

    infoForAccessor = compCombineInfoForAccesor.add_info_for_accesor(
        infoForAccessor,
        "apply on generic bone segmentation",
        datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "Generate glb mesh from dicom",
        generatedGlbPath,
    )
    print(json.dumps(infoForAccessor))
    print(datetime.now())
    compPostToAccesor.sendFilePostRequestToAccessor(infoForAccessor)
    compJobStatus.update_status(jobID, "Finished")
    print(datetime.now())
    compJobCleanup.main(jobID)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
