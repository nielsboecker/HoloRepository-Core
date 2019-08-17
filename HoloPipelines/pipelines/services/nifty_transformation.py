import logging
from nibabel.nifti1 import Nifti1Image
import numpy as np

# TODO: The actual normalising on the numpy data once it's unpacked from
#  nifty1Image should move to numpy_transformation service


def normalise_nifti(image_data: Nifti1Image, new_spacing=[1, 1, 1]):
    """
    After loading a NIfTI file, this function resamples it according to the file headers
    in order to compensate different slice thickness.
    :param image_data: input image data
    :param new_spacing: the desired x-y-z ratio
    :return:  normalised nifti
    """
    # TODO: Why copy??
    image = image_data
    # TODO: does the Nifti1Image have a .shape field? according to documentary, no?
    original_shape = image.shape[:3]

    # TODO: document what happens here
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

    # TODO: Is the image even changed??
    return image