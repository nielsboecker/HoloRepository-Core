import nibabel as nib
import numpy as np
from scipy import ndimage

from core.third_party.ct_lung_segmentation.utils import (
    close_space_dilation,
    generate_initLoc,
    generate_structure_trachea,
)


def segment_airway(params, I, I_affine, Mlung, outputNiftiFolderPath):
    #####################################################
    # Initialize parameters
    #####################################################

    Radius = params["airwayRadiusMask"]
    RadiusX = params["airwayRadiusX"]
    RadiusZ = params["airwayRadiusZ"]
    struct_s = ndimage.generate_binary_structure(3, 1)
    struct_l = ndimage.iterate_structure(struct_s, 3)
    struct_trachea = generate_structure_trachea(Radius, RadiusX, RadiusZ)

    #####################################################
    # Locate an inital point in trachea
    #####################################################

    slice_no, initLoc = generate_initLoc(
        params, I, Mlung, Radius, RadiusZ, struct_trachea
    )

    #####################################################
    # Find airway with closed space diallation
    #####################################################

    Maw = close_space_dilation(
        params, I, Mlung, Radius, RadiusX, RadiusZ, struct_s, slice_no, initLoc
    )

    #####################################################
    # Remove airway & save nii
    #####################################################

    Mawtmp = ndimage.binary_dilation(Maw, structure=struct_l, iterations=1)
    Mawtmp = np.int8(Mawtmp)
    Mlung[Maw > 0] = 0
    nib.Nifti1Image(Maw, I_affine).to_filename(f"{outputNiftiFolderPath}/aw.nii.gz")
    nib.Nifti1Image(Mlung, I_affine).to_filename(f"{outputNiftiFolderPath}/lung.nii.gz")

    return Mlung, Maw
