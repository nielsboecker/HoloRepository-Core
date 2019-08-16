from components import compCommonPath
from components import compDicom2numpy
from components import compNumpy2obj
from components import compObj2glbWrapper
from components import compNumpyTransformation
import pathlib
import sys
import logging
import datetime

logging.basicConfig(level=logging.INFO)


def main(dicomFolderPath, outputGlbPath, threshold):
    generatedNumpyList = compDicom2numpy.main(str(pathlib.Path(dicomFolderPath)))
    resizedNumpyList = compNumpyTransformation.sizeLimit(generatedNumpyList)
    start = datetime.datetime.now()
    generatedObjPath = compNumpy2obj.main(
        resizedNumpyList,
        threshold,
        str(
            compCommonPath.obj.joinpath(
                str(pathlib.PurePath(dicomFolderPath).parts[-1])
            )
        )
        + ".obj",
    )
    end = datetime.datetime.now()
    diff = end - start
    logging.info(
        "time taken for marching cubes:  " + str(diff.total_seconds()) + " seconds"
    )
    generatedGlbPath = compObj2glbWrapper.main(
        generatedObjPath, outputGlbPath, deleteOriginalObj=True, compressGlb=False
    )
    logging.info("dicom2glb: done, glb saved to {}".format(generatedGlbPath))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
