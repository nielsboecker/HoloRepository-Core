"""
This module contains some functions to perform manipulations upon numpy data.
"""

import logging

import numpy as np
import scipy.ndimage

from config import INPUT_RESOLUTION_MAX


# FIXME: This is broken and needs to be fixed @Udomkarn


def crop_around_centre(image: np.ndarray, newX, newY, newZ):
    x, y, z = image.shape

    startX = x // 2 - (newX // 2)
    startY = y // 2 - (newY // 2)
    startZ = z // 2 - (newZ // 2)

    endX = startX + newX
    endY = startY + newY
    endZ = startZ + newZ

    return image[startX:endX, startY:endY, startZ:endZ]


# TODO: Does it make sense? When I already did a downscale such that the longest size
#  is <= the given limit, why would I ever need to then crop it? => @Udomkarn pls fix

# Set limit to prevent crashing of NN containers and general performance issues
def downscale_and_conditionally_crop(
    image: np.ndarray, resolution_limit: int = int(INPUT_RESOLUTION_MAX)
):
    if len(image.shape) >= 3:
        x = image.shape[0]
        y = image.shape[1]
        z = image.shape[2]
    else:
        raise Exception("Invalid array dimension (at least x, y, z)")

    max_side_res = max(x, y, z)
    if max_side_res > resolution_limit:
        resize_ratio = resolution_limit / max_side_res
        image = scipy.ndimage.interpolation.zoom(
            image, [resize_ratio, resize_ratio, resize_ratio]
        )

        x = image.shape[0]
        y = image.shape[1]
        z = image.shape[2]
        max_side_res = max(x, y, z)
        if max_side_res > resolution_limit:
            image = crop_around_centre(
                image, resolution_limit, resolution_limit, resolution_limit
            )
    else:
        logging.info("Array smaller than limit given, no resize has been done")

    return image
