# this pipeline may be removed in the future as obj is not used to display 3D model on hololens
from components import compNifti2numpy
from components import compNumpy2obj
import pathlib
import sys
import numpy as np


def main(inputNiftiPath, outputObjPath, threshold, flipNpy=False):
    generatedNumpyList = compNifti2numpy.main(str(pathlib.Path(inputNiftiPath)))
    generatedObjPath = compNumpy2obj.main(
        generatedNumpyList, threshold, str(pathlib.Path(outputObjPath))
    )
    print("nifti2obj: done")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
