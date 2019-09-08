import os

import nibabel
import numpy
from pytest import fixture

from core.adapters.nifti_file import (
    convert_dicom_np_ndarray_to_nifti_image,
    extract_np_array_from_nifti_image,
    extract_np_array_from_nifti_image_and_normalise,
    read_nifti_as_np_array,
    read_nifti_image,
    write_nifti_image,
)
from core.clients.http import download_and_unzip
from .utils.shared_fixtures import (
    test_input_directory_path,
    test_output_directory_path,
    create_output_directory,
    create_input_directory,
)

minimal_nifti_file_path = "./tests/utils/minimal.nii.gz"
normalised_nifti_file_path = f"{test_input_directory_path}/1103_3_glm.nii"
normalised_nifti_file_zip_download_url = (
    "https://holoblob.blob.core.windows.net/test/1103_3_glm.nii.zip"
)

sample_output_nifti_file_path = f"{test_output_directory_path}/out.nii"


@fixture
def download_nifti_input_file(create_input_directory):
    """
    Downloads a fairly large NIfTI file, which is already normalised.
    """
    if not os.path.isfile(normalised_nifti_file_path):
        download_and_unzip(
            normalised_nifti_file_zip_download_url, test_input_directory_path
        )


def test_read_nifti():
    result = read_nifti_image(minimal_nifti_file_path)
    assert isinstance(result, nibabel.nifti1.Nifti1Image)


def test_read_nifti_as_np_array():
    result = read_nifti_as_np_array(minimal_nifti_file_path)
    assert isinstance(result, numpy.ndarray)


def test_normalise_nifti():
    nifti_image = read_nifti_image(minimal_nifti_file_path)
    initial_nifti_image_as_np = extract_np_array_from_nifti_image(nifti_image)
    assert initial_nifti_image_as_np.shape == (64, 64, 10)

    result = extract_np_array_from_nifti_image_and_normalise(nifti_image)
    assert result.shape == (192, 192, 30)


def test_normalise_nifti_with_already_normalised_input(download_nifti_input_file):
    nifti_image = read_nifti_image(normalised_nifti_file_path)
    initial_nifti_image_as_np = extract_np_array_from_nifti_image(nifti_image)

    result = extract_np_array_from_nifti_image_and_normalise(nifti_image)
    assert result.shape == initial_nifti_image_as_np.shape


def test_write_nifti(create_output_directory):
    nifti_image = read_nifti_image(minimal_nifti_file_path)
    write_nifti_image(nifti_image, sample_output_nifti_file_path)
    assert os.path.exists(sample_output_nifti_file_path)


def test_convert_np_to_nifti():
    nifti_image = read_nifti_image(minimal_nifti_file_path)
    nifti_image_as_np = extract_np_array_from_nifti_image(nifti_image)
    result = convert_dicom_np_ndarray_to_nifti_image(nifti_image_as_np)
    assert isinstance(result, nibabel.nifti1.Nifti1Image)
