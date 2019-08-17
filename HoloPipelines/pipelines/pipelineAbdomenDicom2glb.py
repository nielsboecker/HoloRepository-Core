from components import compDicom2nifti
from pipelines.clients import http
from components import compNifti2numpy
from components import compSeparateNumpy
from components import compNumpyTransformation
from components import compCommonPath
import sys
import logging

logging.basicConfig(level=logging.INFO)


def main(
    inputDicomPath, outputGlbFolderPath, segmentationModelUrl, resolutionLimit=300
):
    generatedNiftiPath = compDicom2nifti.main(
        inputDicomPath, str(compCommonPath.nifti.joinpath("_temp.nii"))
    )
    segmentedNiftiPath = http.send_file_post_request(
        segmentationModelUrl,
        generatedNiftiPath,
        str(compCommonPath.nifti.joinpath("_tempAbdomenSegmented.nii.gz")),
    )
    generatedNumpyList = compNifti2numpy.main(
        segmentedNiftiPath, deleteNiftiWhenDone=True
    )
    resizedNumpyList = compNumpyTransformation.sizeLimit(
        generatedNumpyList, resolutionLimit
    )
    generatedGlbPathList = compSeparateNumpy.main(resizedNumpyList, outputGlbFolderPath)
    logging.info(
        "abdomenDicom2glb: done, glb models generated at "
        + ",".join(generatedGlbPathList)
    )


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]))
