from components import compDicom2nifti_sitk as compDcm2nifti
from components import compJobStatus
from components import compNifti2numpy
from components import compSeparateNumpy
import sys


def main(inputDicomPath, outputGlbFolderPath):
    generatedNiftiPath = compDcm2nifti.main(inputDicomPath, "_temp.nii")
    segmentedNiftiPath = compJobStatus.sendFilePostRequest(
        "http://localhost:5000/model",
        generatedNiftiPath,
        "_tempAbdomenSegmented.nii.gz",
    )
    generatedNumpyList = compNifti2numpy.main(segmentedNiftiPath)
    generatedGlbPathList = compSeparateNumpy.main(
        generatedNumpyList, outputGlbFolderPath
    )
    print(
        "abdomenDicom2glb: done, glb models generated at "
        + ",".join(generatedGlbPathList)
    )


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
