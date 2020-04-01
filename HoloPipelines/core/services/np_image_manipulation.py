"""
This module contains some functions to perform manipulations upon numpy data.
"""

import logging

import numpy as np
import scipy.ndimage

from config import INPUT_RESOLUTION_MAX
from numba import jit

import pirt.interp

@jit
def crop_around_centre(
    image: np.ndarray,
    new_x_dimension_length,
    new_y_dimension_length,
    new_z_dimension_length,
) -> np.ndarray:
    """
    Crop the 3D NumPy array around the centre to a new dimension given as arguments.
    :param image: 3 dimensions NumPy array representing a series of image
    :param new_x_dimension_length: the new X dimension length after cropping
    :param new_y_dimension_length: the new Y dimension length after cropping
    :param new_z_dimension_length: the new Z dimension length after cropping
    :return: numpy ndarray representing the cropped image
    """
    x_dimension_length, y_dimension_length, z_dimension_length = image.shape

    x_start_position = x_dimension_length // 2 - (new_x_dimension_length // 2)
    y_start_position = y_dimension_length // 2 - (new_y_dimension_length // 2)
    z_start_position = z_dimension_length // 2 - (new_z_dimension_length // 2)

    x_end_position = x_start_position + new_x_dimension_length
    y_end_position = y_start_position + new_y_dimension_length
    z_end_position = z_start_position + new_z_dimension_length

    return image[
        x_start_position:x_end_position,
        y_start_position:y_end_position,
        z_start_position:z_end_position,
    ]

def downscale_and_conditionally_crop(
    image: np.ndarray, resolution_limit: int = INPUT_RESOLUTION_MAX
) -> np.ndarray:
    """
    Downscale and crop 3D NumPy array, this is to set limit to prevent crashing of NN containers and general performance issues.
    :param image: 3 dimensions NumPy array representing a series of image
    :param resolution_limit: the resolution limit
    :return: numpy ndarray representing the downscaled and cropped(for the dimension to be divisible by 8 for the NN model) image
    """
    if len(image.shape) >= 3:
        x = image.shape[0]
        y = image.shape[1]
        z = image.shape[2]
    else:
        raise Exception("Invalid array dimension (at least x, y, z)")

    max_side_res = max(x, y, z)
    if max_side_res > resolution_limit:
        resize_ratio = resolution_limit / max_side_res
        image = pirt.interp.zoom(
            image, [resize_ratio, resize_ratio, resize_ratio],order=1
        )
     #   logging.info("Array downscale finished")
    # else:
    #     logging.info("Array smaller than limit given, no downscale has been done")

    x = image.shape[0]
    y = image.shape[1]
    z = image.shape[2]

    # each dimension must be divisible by 8, code below crop the remainder after division by 8
    if (x % 8 != 0) or (y % 8 != 0) or (z % 8 != 0):
        image = crop_around_centre(image, x - (x % 8), y - (y % 8), z - (z % 8))
   #     logging.info("Array not divisible by 8, image cropped")

    return image


def seperate_segmentation(data: np.ndarray, unique_values: list = []) -> np.ndarray:
    """
    Seperate unique values into a new dimension. If no unique values are
    given, np.unique() will be used.
    """
    if not unique_values:
        unique_values = np.unique(data)
    result = np.zeros((len(unique_values), ) + data.shape)
    for i, value in enumerate(unique_values):
        temp = np.array(data)
        temp[temp != value] = 0
        result[i] = temp
    return result
