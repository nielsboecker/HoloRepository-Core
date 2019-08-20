import logging

import numpy as np
import scipy.ndimage

# Set limit to prevent crashing of NN containers and general performance issues
image_resolution_limit = 256


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
def downscale_and_conditionally_crop(
    image: np.ndarray, resolution_limit: int = image_resolution_limit
):
    if len(image.shape) >= 3:
        x = image.shape[0]
        y = image.shape[1]
        z = image.shape[2]
    else:
        raise Exception(
            "compNumpyTransformation: invalid array dimension (at least x, y, z)"
        )

    highest = max(x, y, z)
    if highest > resolution_limit:
        resizeRatio = resolution_limit / highest
        image = scipy.ndimage.interpolation.zoom(
            image, [resizeRatio, resizeRatio, resizeRatio]
        )

        x = image.shape[0]
        y = image.shape[1]
        z = image.shape[2]
        highest = max(x, y, z)
        if highest > resolution_limit:
            image = crop_around_centre(
                image, resolution_limit, resolution_limit, resolution_limit
            )

        logging.info("compNumpyTransformation: array resize done")
    else:
        logging.info(
            "compNumpyTransformation: array smaller than limit given, no resize has been done"
        )
    return image
