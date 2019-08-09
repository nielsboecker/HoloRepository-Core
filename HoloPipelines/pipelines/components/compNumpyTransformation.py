import scipy.ndimage
import sys


def res(img, newX, newY, newZ):
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
            img = res(img, limit, limit, limit)

        print("compNumpyTransformation: array resize done")
    else:
        print(
            "compNumpyTransformation: array smaller than limit given, no resize has been done"
        )
    return img


if __name__ == "__main__":
    print("component can't run on its own")
