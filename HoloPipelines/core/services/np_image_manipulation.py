import logging
import sys

import scipy.ndimage


def crop_around_centre(img, newX, newY, newZ):
    x, y, z = img.shape

    startX = x // 2 - (newX // 2)
    startY = y // 2 - (newY // 2)
    startZ = z // 2 - (newZ // 2)

    endX = startX + newX
    endY = startY + newY
    endZ = startZ + newZ

    return img[startX:endX, startY:endY, startZ:endZ]


# TODO: Does it make sense? When I already did a downscale such that the longest size
#  is <= the given limit, why would I ever need to then crop it?
def downscale_and_conditionally_crop(img, limit):
    if len(img.shape) >= 3:
        x = img.shape[0]
        y = img.shape[1]
        z = img.shape[2]
    else:
        # TODO: Exit, really???
        sys.exit("compNumpyTransformation: invalid array dimension (at least x, y, z)")
    highest = max(x, y, z)
    if highest > limit:
        resizeRatio = limit / highest
        img = scipy.ndimage.interpolation.zoom(
            img, [resizeRatio, resizeRatio, resizeRatio]
        )

        x = img.shape[0]
        y = img.shape[1]
        z = img.shape[2]
        highest = max(x, y, z)
        if highest > limit:
            img = crop_around_centre(img, limit, limit, limit)

        logging.info("compNumpyTransformation: array resize done")
    else:
        logging.info(
            "compNumpyTransformation: array smaller than limit given, no resize has been done"
        )
    return img
