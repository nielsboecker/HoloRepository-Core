import glob
import os
import pathlib
import sys

import nibabel as nib

import core.third_party.ct_lung_segmentation.utils as utils
from core.third_party.ct_lung_segmentation.segment_airway import segment_airway
from core.third_party.ct_lung_segmentation.segment_lung import segment_lung


def perform_lung_segmentation(inputNiftiPath, outputNiftiFolderPath):
    inputNiftiPath = str(pathlib.Path(inputNiftiPath))
    if not os.path.exists(outputNiftiFolderPath):
        os.makedirs(outputNiftiFolderPath)

    params = utils.define_parameter()

    # TODO: File, not folder
    if os.path.isdir(inputNiftiPath):
        lsdir = glob.glob(str(pathlib.Path(inputNiftiPath).joinpath("*.nii.gz")))
        if len(lsdir) != 1:
            sys.exit(
                "ct_lung_segmentation.main: error, invalid number of Nifti file found inside folder "
                + inputNiftiPath
            )
        inputNiftiPath = str(pathlib.Path(lsdir[0]))

    # Load image
    image = nib.load(inputNiftiPath)
    image_affine = image.affine
    image_data = image.get_data()

    # Coarse segmentation of lung & airway
    # Note: Skips writing "lungaw.nii.gz" to disk, but still needs to be run as the result is a
    # required argument for the next step
    Mlung = segment_lung(params, image_data, image_affine)

    # Romove airway from lung mask
    # Note: This step generates the "lung.nii.gz" and "aw.nii.gz" files
    Mlung, Maw = segment_airway(
        params, image_data, image_affine, Mlung, outputNiftiFolderPath
    )

    # TODO: Could be refactored. File saving can be done here on this level, and moved to nifti_file adapter
    # Or the write/read again can maybe be avoided if the result variables are returned instead

    # TODO: Could be refactored, having an airway pipeline is exactly the same, just return different output
    return str(pathlib.Path(outputNiftiFolderPath).joinpath("lung.nii.gz"))
