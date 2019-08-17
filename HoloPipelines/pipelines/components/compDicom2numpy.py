import numpy as np
import pydicom as dicom
import os
import scipy.ndimage
import SimpleITK as sitk
import pathlib
import sys
import logging

logging.basicConfig(level=logging.INFO)


def load_scan(scan_path):
    slices = [
        dicom.read_file(str(pathlib.Path(scan_path, s)))
        for s in os.listdir(str(scan_path))
    ]
    slices.sort(key=lambda x: int(x.InstanceNumber))
    try:
        slick_thickness = np.abs(
            slices[0].ImagePositionscan[2] - slices[1].ImagePositionscan[2]
        )

    except Exception as e:
        logging.warning(
            "Unable to load slice's image positon, using slice location instead: {}".format(
                str(e)
            )
        )
        slick_thickness = np.abs(slices[0].SliceLocation - slices[1].SliceLocation)

    for s in slices:
        s.SliceThickness = slick_thickness

    return slices


def load_pixel_array(input_path):
    reader = sitk.ImageSeriesReader()

    dicom_name = reader.GetGDCMSeriesFileNames(input_path)
    reader.SetFileNames(dicom_name)

    image = reader.Execute()
    numpy_array_image = sitk.GetArrayFromImage(image)

    return numpy_array_image


def resample(data_path, new_spacing=[1, 1, 1]):
    scan = load_scan(data_path)
    image = load_pixel_array(data_path)
    logging.info("Shape before resampling\t" + repr(image.shape))
    # Determine current pixel spacing
    try:
        spacing = map(
            float,
            (
                [scan[0].SliceThickness]
                + [scan[0].PixelSpacing[0], scan[0].PixelSpacing[1]]
            ),
        )
        spacing = np.array(list(spacing))
    except Exception as e:
        logging.warning(
            "Unable to load elements of PixelSpacing from dicom, please make sure header data exist. scan[0].PixelSpacing: "
            + len(scan[0].PixelSpacing)
        )
        logging.warning(
            "Pixel Spacing (row, col): (%f, %f) "
            % (scan[0].PixelSpacing[0], scan[0].PixelSpacing[1])
        )
        sys.exit("dicom2numpy: error loading scan: {}".format(str(e)))

    # calculate resize factor
    resize_factor = spacing / new_spacing
    new_real_shape = image.shape * resize_factor
    new_shape = np.round(new_real_shape)
    real_resize_factor = new_shape / image.shape
    new_spacing = spacing / real_resize_factor

    image = scipy.ndimage.interpolation.zoom(image, real_resize_factor)
    logging.info("Shape after resampling\t" + repr(image.shape))

    return image, new_spacing


def reorientateNumpyList(numpyList):
    # transpose numpy i.e. (z, y, x) ---> (x, y, z)
    numpyList = numpyList.transpose(2, 1, 0)
    numpyList = np.flip(numpyList, 0)
    numpyList = np.flip(numpyList, 1)
    return numpyList


def main(dicom_path):
    logging.info("dicom2numpy: resampling dicom...")
    imgs_after_resamp, spacing = resample(dicom_path)
    logging.info("dicom2numpy: resampling done")
    imgs_after_resamp = reorientateNumpyList(imgs_after_resamp)
    return imgs_after_resamp


if __name__ == "__main__":
    logging.error("component can't run on its own")
