"""
This module provides a wrapper around the existing ct_lung_segmentation implementation.
"""
import logging
import nibabel as nib
import numpy as np

import core.third_party.ct_lung_segmentation.utils as utils
from core.third_party.ct_lung_segmentation.segment_airway import segment_lung_airway
from core.third_party.ct_lung_segmentation.segment_lung import segment_lung


def perform_lung_segmentation(image_data: np.ndarray) -> str:
    """
    Calls the implementation of lung segmentation and returns path to the result file.
    """
    logging.info("Performing lung segmentation...")
    params = utils.define_parameter()
    image_affine = np.eye(4)

    # Coarse segmentation of lung & airway
    # Note: Skips writing "lungaw.nii.gz" to disk, but still needs to be run as the result is a
    # required argument for the next step
    segmented_lung_and_airway = segment_lung(params, image_data, image_affine)

    # Romove airway from lung mask
    # Note: This step generates the "lung.nii.gz" and "aw.nii.gz" files
    segmented_lung, segmented_airway = segment_lung_airway(
        params, image_data, image_affine, segmented_lung_and_airway
    )

    logging.info("Finished lung segmentation")

    return segmented_lung, segmented_airway
