"""
This module provides a wrapper around the existing ct_lung_segmentation implementation.
"""

import nibabel as nib

import core.third_party.ct_lung_segmentation.utils as utils
from core.third_party.ct_lung_segmentation.segment_airway import segment_airway
from core.third_party.ct_lung_segmentation.segment_lung import segment_lung


def perform_lung_segmentation(
    input_nifti_file_path: str, output_nifti_directory_path: str
) -> str:
    """
    Calls the implementation of lung segmentation and returns path to the result file.
    """
    params = utils.define_parameter()

    # Load image
    image = nib.load(input_nifti_file_path)
    image_affine = image.affine
    image_data = image.get_data()

    # Coarse segmentation of lung & airway
    # Note: Skips writing "lungaw.nii.gz" to disk, but still needs to be run as the result is a
    # required argument for the next step
    segmented_lung = segment_lung(params, image_data, image_affine)

    # Romove airway from lung mask
    # Note: This step generates the "lung.nii.gz" and "aw.nii.gz" files
    segmented_lung, segmented_airway = segment_airway(
        params, image_data, image_affine, segmented_lung, output_nifti_directory_path
    )

    # TODO: Could be refactored. File saving can be done here on this level, and use
    #  nifti_file adapter functionality
    # Or the write/read again can maybe be avoided if the result variables are returned instead

    # TODO: Could be refactored, having an airway pipeline is exactly the same, just return different output
    return f"{output_nifti_directory_path}/lung.nii.gz"
