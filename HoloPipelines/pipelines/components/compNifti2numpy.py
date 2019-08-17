import numpy as np
import nibabel as nib
import os
import logging

logging.basicConfig(level=logging.INFO)


def resample(image_data, new_spacing=[1, 1, 1]):
    image = image_data
    original_shape = image.shape[:3]

    image._affline = None
    spacing = map(
        float,
        (
                [list(image.header.get_zooms())[2]]
                + [list(image.header.get_zooms())[0], list(image.header.get_zooms())[1]]
        ),
    )
    spacing = np.array(list(spacing))

    resize_factor = spacing / new_spacing
    new_real_shape = image.shape[:3] * resize_factor
    new_shape = np.round(new_real_shape)
    real_resize_factor = new_shape / image.shape[:3]
    # TODO: Why overriding variable? And also why is it unused anyway, afterwards?
    new_spacing = spacing / real_resize_factor

    logging.info("Shape before resampling\t" + repr(original_shape))
    logging.info("Shape after resampling\t" + repr(image.shape[:3]))

    return image


def main(input_nifti_path, deleteNiftiWhenDone=False):
    # https://github.com/nipy/nibabel/issues/626
    nib.Nifti1Header.quaternion_threshold = -1e-06
    img = nib.load(input_nifti_path)

    img = resample(img)

    numpyList = np.array(img.dataobj)

    if deleteNiftiWhenDone:
        os.remove(input_nifti_path)

    return numpyList
