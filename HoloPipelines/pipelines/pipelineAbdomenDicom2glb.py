import pipelines.services.format_conversion
from pipelines.services import format_conversion
from pipelines.clients import http
from pipelines.tasks.abdominal_organs_segmentation import split_to_separate_organs
from pipelines.services.np_image_manipulation import downscale_and_conditionally_crop
from pipelines.services.format_conversion import convert_nifty_to_numpy_and_normalise
from pipelines.config.io_paths import nifti_path

import sys
import logging

logging.basicConfig(level=logging.INFO)


def main(
    inputDicomPath, outputGlbFolderPath, segmentationModelUrl, resolutionLimit=300
):
    generatedNiftiPath = format_conversion.convert_dicom_to_nifty(
        inputDicomPath, str(nifti_path.joinpath("_temp.nii"))
    )
    segmentedNiftiPath = http.send_file_post_request(
        segmentationModelUrl,
        generatedNiftiPath,
        str(nifti_path.joinpath("_tempAbdomenSegmented.nii.gz")),
    )
    generatedNumpyList = convert_nifty_to_numpy_and_normalise(segmentedNiftiPath)
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
