import scipy.ndimage
import sys
import logging

logging.basicConfig(level=logging.INFO)


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


# TODO: This is fro the nifty2numpy component. So initially that other file reads nifty.
# But essentially this method here performs numpy manipulations. Find out what it does semantically
# and give a better name
def resample_from_nifty2numpy(image_data, new_spacing=[1, 1, 1]):
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