from typing import List

import numpy as np
import pydicom
import os
import scipy.ndimage
import SimpleITK as sitk
import pathlib
import sys
import logging

logging.basicConfig(level=logging.INFO)


def read_dicom_dataset(scan_path):
    slices = [
        pydicom.read_file(str(pathlib.Path(scan_path, s)))
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


def read_dicom_pixel_array(input_path):
    reader = sitk.ImageSeriesReader()

    dicom_name = reader.GetGDCMSeriesFileNames(input_path)
    reader.SetFileNames(dicom_name)

    image = reader.Execute()
    numpy_array_image = sitk.GetArrayFromImage(image)

    return numpy_array_image


def normalise_dicom(data_path, new_spacing=[1, 1, 1]):
    dicom_dataset: List[pydicom.dataset.FileDataset] = read_dicom_dataset(data_path)
    dicom_sample_slice = dicom_dataset[0]
    dicom_image_array: np.ndarray = read_dicom_pixel_array(data_path)

    logging.info("Shape before resampling\t" + repr(dicom_image_array.shape))
    # Determine current pixel spacing
    try:
        spacing = map(
            float,
            (
                [dicom_sample_slice.SliceThickness]
                + [dicom_sample_slice.PixelSpacing[0], dicom_sample_slice.PixelSpacing[1]]
            ),
        )
        spacing = np.array(list(spacing))
    except Exception as e:
        logging.warning(
            "Unable to load elements of PixelSpacing from dicom, please make sure header data exist. dicom_dataset[0].PixelSpacing: "
            + str(len(dicom_sample_slice.PixelSpacing))
        )
        logging.warning(
            "Pixel Spacing (row, col): (%f, %f) "
            % (dicom_sample_slice.PixelSpacing[0], dicom_sample_slice.PixelSpacing[1])
        )
        sys.exit("dicom2numpy: error loading dicom_dataset: {}".format(str(e)))

    # calculate resize factor
    resize_factor = spacing / new_spacing
    new_real_shape = dicom_image_array.shape * resize_factor
    new_shape = np.round(new_real_shape)
    real_resize_factor = new_shape / dicom_image_array.shape
    new_spacing = spacing / real_resize_factor

    dicom_image_array = scipy.ndimage.interpolation.zoom(dicom_image_array, real_resize_factor)
    logging.info("Shape after resampling\t" + repr(dicom_image_array.shape))

    return dicom_image_array


def flip_numpy_array_dimensions(numpyList):
    # transpose numpy i.e. (z, y, x) ---> (x, y, z)
    numpyList = numpyList.transpose(2, 1, 0)
    numpyList = np.flip(numpyList, 0)
    numpyList = np.flip(numpyList, 1)
    return numpyList


def convert_dicom_to_numpy_and_normalise(dicom_path):
    logging.info("dicom2numpy: resampling dicom...")
    imgs_after_resamp = normalise_dicom(dicom_path)
    logging.info("dicom2numpy: resampling done")
    imgs_after_resamp = flip_numpy_array_dimensions(imgs_after_resamp)
    return imgs_after_resamp
