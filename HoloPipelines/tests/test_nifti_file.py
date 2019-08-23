# import pytest
# import os
# import numpy as np
import nibabel
from core.adapters.nifti_file import (
    extract_np_array_from_nifti_image,
    extract_np_array_from_nifti_image_and_normalise,
    read_nifti_image,
)

# read_nifti_as_np_array,
# write_nifti_image,
# convert_dicom_np_ndarray_to_nifti_image,

# read nifti


def test_read_nifti():
    nifti_image = read_nifti_image(
        "/Users/apple/Desktop/itkTest/abdomenFromOwen.nii"
    )  # TODO: update this, actually dl it from somewhere
    assert isinstance(nifti_image, nibabel.nifti1.Nifti1Image)


# normalise nifti that is already normalised (so the shape has to be the same after rescaling)
def test_normalise_nifti():
    nifti_image = read_nifti_image("/Users/apple/Desktop/itkTest/abdomenFromOwen.nii")
    nifti_image_as_np = extract_np_array_from_nifti_image(nifti_image)

    normalised_nifti_image_as_np = extract_np_array_from_nifti_image_and_normalise(
        nifti_image
    )
    assert (
        normalised_nifti_image_as_np.shape == nifti_image_as_np.shape
    )  # TODO: double check that the nifti is already normalised
