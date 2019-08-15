import scipy.ndimage
import sys
import logging

logging.basicConfig(level=logging.INFO)


def centerCrop(img, newX, newY, newZ):
    x, y, z = img.shape

    startX = x // 2 - (newX // 2)
    startY = y // 2 - (newY // 2)
    startZ = z // 2 - (newZ // 2)

    endX = startX + newX
    endY = startY + newY
    endZ = startZ + newZ

    return img[startX:endX, startY:endY, startZ:endZ]


def sizeLimit(img, limit):
    if len(img.shape) >= 3:
        x = img.shape[0]
        y = img.shape[1]
        z = img.shape[2]
    else:
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
            img = centerCrop(img, limit, limit, limit)

        logging.info("compNumpyTransformation: array resize done")
    else:
        logging.info(
            "compNumpyTransformation: array smaller than limit given, no resize has been done"
        )
    return img


if __name__ == "__main__":
    logging.error("component can't run on its own")
