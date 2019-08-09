from components import compDicom2nifti
from components import compHttpRequest
from components import compNifti2numpy
from components import compSeparateNumpy
from components import compNumpyTransformation
import sys


def main(inputDicomPath, outputGlbFolderPath, segmentationModelUrl):
    generatedNiftiPath = compDicom2nifti.main(inputDicomPath, "_temp.nii")
    segmentedNiftiPath = compHttpRequest.sendFilePostRequest(
        segmentationModelUrl, generatedNiftiPath, "_tempAbdomenSegmented.nii.gz"
    )
    generatedNumpyList = compNifti2numpy.main(segmentedNiftiPath)
    resizedNumpyList = compNumpyTransformation.sizeLimit(generatedNumpyList, 300)
    generatedGlbPathList = compSeparateNumpy.main(resizedNumpyList, outputGlbFolderPath)
    print(
        "abdomenDicom2glb: done, glb models generated at "
        + ",".join(generatedGlbPathList)
    )


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
