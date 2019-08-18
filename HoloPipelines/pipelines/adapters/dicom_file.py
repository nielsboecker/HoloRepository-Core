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


def read_dicom_dataset(input_path: str):
    """
    Reads a DICOM file and returns a pydicom representation, used to obtain knowledge about the
    slice thickness, that can then e.g. be used to manipulate image data.
    :param input_path: Path to the DICOM file
    :return: pydicom.dataset.FileDataset representing the DICOM file
    """
    slices = [
        pydicom.read_file(str(pathlib.Path(input_path, s)))
        for s in os.listdir(str(input_path))
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


def read_dicom_pixels_as_np_ndarray(input_path):
    """
    Reads a DICOM image and returns it as a numpy ndarray. The method will always call
    flip_numpy_array_dimensions() to mirror the dimensions and return accurate data.
    :param input_path: Path to the DICOM file
    :return: numpy ndarray representing the DICOM file
    """
    reader = sitk.ImageSeriesReader()

    dicom_name = reader.GetGDCMSeriesFileNames(input_path)
    reader.SetFileNames(dicom_name)

    image = reader.Execute()
    numpy_array_image = sitk.GetArrayFromImage(image)
    fixed_numpy_array_image = flip_numpy_array_dimensions(numpy_array_image)

    return fixed_numpy_array_image


def flip_numpy_array_dimensions(array: np.ndarray):
    """
    Transposes and flips numpy axes, i.e. (z, y, x) ---> (x, y, z). This is needed as the default
    data when we read it is "mirrored" and therefore not accurate and, e.g., not valid as input
    for pre-trained NN models.
    :param array: ndarray from pydicom.read_file()
    :return: array with flipped axis to represent the accurate DICOM data
    """
    array = array.transpose((2, 1, 0))
    array = np.flip(array, 0)
    array = np.flip(array, 1)
    return array


def normalise_dicom(dicom_image_array: np.ndarray, input_path: str):
    """
    Compensates the distortion caused by slice thickness, using data obtained from the DICOM header
    :param dicom_image_array: numpy ndarray representing the DICOM file
    :param input_path: Path to the DICOM file
    :return: normalised dicom_image_array
    """
    dicom_dataset: List[pydicom.dataset.FileDataset] = read_dicom_dataset(input_path)
    dicom_sample_slice = dicom_dataset[0]

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
    except Exception:
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
    new_spacing = [1, 1, 1]
    resize_factor = spacing / new_spacing
    new_real_shape = dicom_image_array.shape * resize_factor
    new_shape = np.round(new_real_shape)
    real_resize_factor = new_shape / dicom_image_array.shape

    dicom_image_array = scipy.ndimage.interpolation.zoom(dicom_image_array, real_resize_factor)
    logging.info("Shape after resampling\t" + repr(dicom_image_array.shape))

    return dicom_image_array


def read_dicom_as_np_ndarray_and_normalise(input_path: str):
    dicom_image: np.ndarray = read_dicom_pixels_as_np_ndarray(input_path)
    normalised_dicom_image: np.ndarray = normalise_dicom(dicom_image, input_path)
    return normalised_dicom_image
