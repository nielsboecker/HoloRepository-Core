from pipelines.adapters.dicom_file import read_dicom_as_np_ndarray_and_normalise
from pipelines.adapters.nifti_file import read_nifti_as_np_array_and_normalise, write_nifti_image, \
    convert_dicom_np_ndarray_to_nifti_image
from pipelines.clients import http
from pipelines.tasks.abdominal_organs_segmentation.split_to_separate_organs import split_to_separate_organs
from pipelines.services.np_image_manipulation import downscale_and_conditionally_crop
from pipelines.config.io_paths import nifti_path

import sys
import logging


def main(
    inputDicomPath, outputGlbFolderPath, segmentationModelUrl, resolutionLimit=300
):
    dicom_image_array = read_dicom_as_np_ndarray_and_normalise(inputDicomPath)
    nifti_image = convert_dicom_np_ndarray_to_nifti_image(dicom_image_array)

    nifti_output_path = str(nifti_path.joinpath("_temp.nii"))
    write_nifti_image(nifti_image, nifti_output_path)

    segmentedNiftiPath = http.send_file_post_request(
        segmentationModelUrl,
        nifti_output_path,
        str(nifti_path.joinpath("_tempAbdomenSegmented.nii.gz")),
    )
    generatedNumpyList = read_nifti_as_np_array_and_normalise(segmentedNiftiPath)
    resizedNumpyList = downscale_and_conditionally_crop(
        generatedNumpyList, resolutionLimit
    )
    generatedGlbPathList = split_to_separate_organs(resizedNumpyList, outputGlbFolderPath)
    logging.info(
        "abdomenDicom2glb: done, glb models generated at "
        + ",".join(generatedGlbPathList)
    )


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]))
