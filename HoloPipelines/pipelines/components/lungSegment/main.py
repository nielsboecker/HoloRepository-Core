import nibabel as nib
import pathlib
import os
import glob
import sys


def main(inputNiftiPath, outputNiftiFolderPath):
    inputNiftiPath = str(pathlib.Path(inputNiftiPath))
    if not os.path.exists(outputNiftiFolderPath):
        os.makedirs(outputNiftiFolderPath)

    import components.lungSegment.utils as utils
    from components.lungSegment.segment_lung import segment_lung
    from components.lungSegment.segment_airway import segment_airway

    params = utils.define_parameter()

    if os.path.isdir(inputNiftiPath):
        lsdir = glob.glob(str(pathlib.Path(inputNiftiPath).joinpath("*.nii.gz")))
        if len(lsdir) != 1:
            sys.exit(
                "lungSegment.main: error, invalid number of Nifti file found inside folder "
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


if __name__ == "__main__":
    print("component can't run on its own")
