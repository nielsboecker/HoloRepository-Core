from components import compNifti2numpy
from components import compNumpy2obj
from components import compObj2glbWrapper
import pathlib
import sys


def main(inputNiftiPath, outputGlbPath, threshold):
    generatedNumpyList = compNifti2numpy.main(str(pathlib.Path(inputNiftiPath)))
    generatedObjPath = compNumpy2obj.main(
        generatedNumpyList,
        threshold,
        str(pathlib.Path.cwd().joinpath("output", "OBJ", "nifti2glb_tempObj.obj")),
    )
    generatedGlbPath = compObj2glbWrapper.main(
        generatedObjPath,
        str(pathlib.Path(outputGlbPath)),
        deleteOriginalObj=True,
        compressGlb=False,
    )
    print("nifti2glb: done")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
