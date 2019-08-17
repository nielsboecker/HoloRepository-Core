# this pipeline may be removed in the future as obj is not used to display 3D model on hololens
from pipelines.components import compNifti2numpy
from pipelines.components import compNumpy2obj
import pathlib
import sys
import logging

logging.basicConfig(level=logging.INFO)


def main(inputNiftiPath, outputObjPath, threshold, flipNpy=False):
    generatedNumpyList = compNifti2numpy.main(str(pathlib.Path(inputNiftiPath)))
    generatedObjPath = compNumpy2obj.main(
        generatedNumpyList, threshold, str(pathlib.Path(outputObjPath))
    )
    logging.info("nifti2obj: done, obj saved to {}".format(generatedObjPath))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
