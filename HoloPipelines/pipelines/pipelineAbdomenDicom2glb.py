from components import compDicom2nifti
from components import compHttpRequest
from components import compNifti2numpy
from components import compSeparateNumpy
from components import compNumpyTransformation
from components import compCommonPath
import sys
import logging

logging.basicConfig(level=logging.INFO)


def main(inputDicomPath, outputGlbFolderPath, segmentationModelUrl):
    generatedNiftiPath = compDicom2nifti.main(
        inputDicomPath, str(compCommonPath.nifti.joinpath("_temp.nii"))
    )
    segmentedNiftiPath = compHttpRequest.sendFilePostRequest(
        segmentationModelUrl,
        generatedNiftiPath,
        str(compCommonPath.nifti.joinpath("_tempAbdomenSegmented.nii.gz")),
    )
    generatedNumpyList = compNifti2numpy.main(
        segmentedNiftiPath, deleteNiftiWhenDone=True
    )
    resizedNumpyList = compNumpyTransformation.sizeLimit(generatedNumpyList)
    generatedGlbPathList = compSeparateNumpy.main(resizedNumpyList, outputGlbFolderPath)
    logging.info(
        "abdomenDicom2glb: done, glb models generated at "
        + ",".join(generatedGlbPathList)
    )


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
