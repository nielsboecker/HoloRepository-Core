import numpy as np
import nibabel as nib
import os
import logging

logging.basicConfig(level=logging.INFO)


def resample(imageData, new_spacing=[1, 1, 1]):
    image = imageData
    originalShape = image.shape[:3]
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
    new_spacing = spacing / real_resize_factor

    logging.info("Shape before resampling\t", originalShape)
    logging.info("Shape after resampling\t", image.shape[:3])

    return image, new_spacing


def main(inputNiftiPath, deleteNiftiWhenDone=False):
    # https://github.com/nipy/nibabel/issues/626
    nib.Nifti1Header.quaternion_threshold = -1e-06
    img = nib.load(inputNiftiPath)

    img, newSpacing = resample(img)

    numpyList = np.array(img.dataobj)

    if deleteNiftiWhenDone:
        os.remove(inputNiftiPath)

    return numpyList


if __name__ == "__main__":
    logging.error("component can't run on its own")
