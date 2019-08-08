import scipy.ndimage


def crop(img, cropx, cropy, cropz):
    x, y, z = img.shape

    startX = x // 2 - (cropx // 2)
    startY = y // 2 - (cropy // 2)
    startZ = z // 2 - (cropz // 2)

    endX = startX + cropx
    endY = startY + cropy
    endZ = startZ + cropz

    return img[startX:endX, startY:endY, startZ:endZ]


def resize(img, ratioX, ratioY, ratioZ):
    return scipy.ndimage.interpolation.zoom(img, [ratioX, ratioY, ratioZ])


def sizeLimit(img, limit):
    x, y, z = img.shape
    highest = max(x, y, z)
    if highest > limit:
        rezieRatio = limit / highest
        img = resize(img, rezieRatio, rezieRatio, rezieRatio)

        x, y, z = img.shape
        highest = max(x, y, z)
        if highest > limit:
            img = crop(img, limit, limit, limit)

        print("array resize done")
    else:
        print("array smaller than limit given, no resize has been done")
    return img


if __name__ == "__main__":
    print("component can't run on its own")
