"""
This module contains functionality related to reading and transforming DICOM files.
"""

import logging
import os
from multiprocessing.pool import ThreadPool
from typing import List

import SimpleITK as sitk
import numpy as np
import pydicom
import scipy.ndimage
import pirt.interp
from numba import njit,jit


def read_dicom_dataset(input_directory_path: str) -> List[pydicom.dataset.FileDataset]:
    """
    Reads a DICOM file and returns a pydicom representation, used to obtain knowledge
    about the slice thickness, that can then e.g. be used to manipulate image data.
    :param input_directory_path: Path to the directory containing the individual DICOM files
    :return: List[pydicom.dataset.FileDataset] representing the DICOM file
    """
    slices: List[pydicom.dataset.FileDataset] = [
        pydicom.read_file(f"{input_directory_path}/{dcm_file}")
        for dcm_file in os.listdir(input_directory_path)
    ]
    slices.sort(key=lambda x: int(x.InstanceNumber))

    # Ensure that SliceThickness is set for all slices
    try:
        slice_thickness = np.abs(
            slices[0].ImagePositionPatient[2] - slices[1].ImagePositionPatient[2]
        )
    except AttributeError:
        logging.info("ImagePositionPatient is not set, using SliceLocation instead.")
        slice_thickness = np.abs(slices[0].SliceLocation - slices[1].SliceLocation)

    for s in slices:
        s.SliceThickness = slice_thickness

    return slices


def read_dicom_pixels_as_np_ndarray(input_file_path: str) -> np.ndarray:
    """
    Reads a DICOM image and returns it as a numpy ndarray. The method will always call
    flip_numpy_array_dimensions() to mirror the dimensions and return accurate data.
    :param input_file_path: Path to the DICOM file
    :return: numpy ndarray representing the DICOM file
    """
    reader = sitk.ImageSeriesReader()

    dicom_name = reader.GetGDCMSeriesFileNames(input_file_path)
    reader.SetFileNames(dicom_name)

    # image = reader.Execute()
    #
    # numpy_array_image = sitk.GetArrayFromImage(image)
    # fixed_numpy_array_image = flip_numpy_array_dimensions(numpy_array_image)

    p = ThreadPool()
    result = p.map(load_file, dicom_name)
    p.close()
    p.join()
    result = np.asarray(result)

    numpy_array_image = result
    fixed_numpy_array_image = flip_numpy_array_dimensions(numpy_array_image)

    return fixed_numpy_array_image


def flip_numpy_array_dimensions(array: np.ndarray) -> np.ndarray:
    """
    Transposes numpy axes, i.e. (z, y, x) ---> (x, y, z), and flips x axis. This is
    needed as the default data when we read it is "mirrored" and therefore not accurate
    and, e.g., not valid as input for pre-trained NN models.
    :param array: ndarray from pydicom.read_file()
    :return: array with flipped axis to represent the accurate DICOM data
    """
    array = array.transpose((2, 1, 0))
    array = np.flip(array, 0)
    return array


def flip_numpy_array_dimensions_y_only(array: np.ndarray) -> np.ndarray:
    """
    Flip y axis in numpy array.
    :param array: ndarray from pydicom.read_file()
    :return: array with flipped y axis to represent the accurate DICOM data
    """
    array = np.flip(array, 1)
    return array

def normalise_dicom(dicom_image_array: np.ndarray, input_file_path: str) -> np.ndarray:
    """
    Compensates the distortion caused by slice thickness, using data obtained from the DICOM header
    :param dicom_image_array: numpy ndarray representing the DICOM file
    :param input_file_path: Path to the DICOM file
    :return: normalised dicom_image_array
    """
    dicom_dataset: List[pydicom.dataset.FileDataset] = read_dicom_dataset(
        input_file_path
    )
    dicom_sample_slice = dicom_dataset[0]

    logging.info("Normalising DICOM image to compensate slice thickness distortion")
    logging.info(f"Shape before normalising: {dicom_image_array.shape}")

    # Determine current pixel spacing
    try:
        spacing = map(
            float,
            (
                [dicom_sample_slice.SliceThickness]
                + [
                    dicom_sample_slice.PixelSpacing[0],
                    dicom_sample_slice.PixelSpacing[1],
                ]
            ),
        )
        spacing = np.array(list(spacing))
    except AttributeError as e:
        # Apparently this can happen when PixelSpacing header doesn't exist
        # Not sure if the actual exception is useful enough so adding extra infos
        raise AttributeError(
            f"Error while loading DICOM, maybe due to " f"PixelSpacing: {e}"
        )

    # calculate resize factor
    new_spacing = [1, 1, 1]
    resize_factor = spacing / new_spacing
    new_real_shape = dicom_image_array.shape * resize_factor
    new_shape = np.round(new_real_shape)

    real_resize_factor = new_shape / dicom_image_array.shape
    real_resize_factor = np.flip(real_resize_factor, 0)

    dicom_image_array = normalizetest(dicom_image_array, real_resize_factor)
    logging.info(f"Shape after normalising: {dicom_image_array.shape}")

    return dicom_image_array


def load_file(path):
    file_reader = sitk.ImageFileReader()
    file_reader.SetFileName(path)
    image = file_reader.Execute()
    image_np = sitk.GetArrayFromImage(image)
    return np.squeeze(image_np)



@jit
def normalizetest( dicom_image_array, real_resize_factor):
    return pirt.interp.zoom(
        dicom_image_array, np.ndarray.tolist(real_resize_factor), order=0
    )


def read_dicom_as_np_ndarray_and_normalise(input_directory_path: str) -> np.ndarray:
    dicom_image = read_dicom_pixels_as_np_ndarray(input_directory_path)
    normalised_dicom_image = normalise_dicom(dicom_image, input_directory_path)
    return normalised_dicom_image
