import nibabel as nib
import pathlib
import os
import glob
import sys
import pipelines.third_party.ct_lung_segmentation.utils as utils
from pipelines.third_party.ct_lung_segmentation.segment_lung import segment_lung
from pipelines.third_party.ct_lung_segmentation.segment_airway import segment_airway

def perform_lung_segmentation(inputNiftiPath, outputNiftiFolderPath):
    inputNiftiPath = str(pathlib.Path(inputNiftiPath))
    if not os.path.exists(outputNiftiFolderPath):
        os.makedirs(outputNiftiFolderPath)


    params = utils.define_parameter()

    if os.path.isdir(inputNiftiPath):
        lsdir = glob.glob(str(pathlib.Path(inputNiftiPath).joinpath("*.nii.gz")))
        if len(lsdir) != 1:
            sys.exit(
                "ct_lung_segmentation.main: error, invalid number of Nifti file found inside folder "
                + inputNiftiPath
            )
        inputNiftiPath = str(pathlib.Path(lsdir[0]))

    #####################################################
    # Load image
    #####################################################

    image = nib.load(inputNiftiPath)
    I_affine = image.affine
    image = image.get_data()

    #####################################################
    # Coarse segmentation of lung & airway
    #####################################################

    Mlung = segment_lung(params, image, I_affine, outputNiftiFolderPath)

    #####################################################
    # Romove airway from lung mask
    #####################################################

    Mlung, Maw = segment_airway(params, image, I_affine, Mlung, outputNiftiFolderPath)

    return str(pathlib.Path(outputNiftiFolderPath).joinpath("lung.nii.gz"))
