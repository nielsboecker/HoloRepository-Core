import os

import nibabel
import numpy

from core.adapters.nifti_file import (
    convert_dicom_np_ndarray_to_nifti_image,
    extract_np_array_from_nifti_image,
    extract_np_array_from_nifti_image_and_normalise,
    read_nifti_as_np_array,
    read_nifti_image,
    write_nifti_image,
)
from .utils.shared_fixtures import create_output_directory

sample_nifti_file_path = "./tests/utils/minimal.nii.gz"
test_output_path = "./__test_output__"
sample_output_nifti_file_path = f"{test_output_path}/out.nii"


def test_read_nifti():
    result = read_nifti_image(sample_nifti_file_path)
    assert isinstance(result, nibabel.nifti1.Nifti1Image)


def test_read_nifti_as_np_array():
    result = read_nifti_as_np_array(sample_nifti_file_path)
    assert isinstance(result, numpy.ndarray)


def test_normalise_nifti():
    nifti_image = read_nifti_image(sample_nifti_file_path)
    initial_nifti_image_as_np = extract_np_array_from_nifti_image(nifti_image)
    assert initial_nifti_image_as_np.shape == (64, 64, 10)

    result = extract_np_array_from_nifti_image_and_normalise(nifti_image)
    #  nifti is already normalised (so the shape has to be the same after rescaling)
    assert result.shape == (192, 192, 30)


def test_write_nifti(create_output_directory):
    nifti_image = read_nifti_image(sample_nifti_file_path)
    write_nifti_image(nifti_image, sample_output_nifti_file_path)
    assert os.path.exists(sample_output_nifti_file_path)


def test_convert_np_to_nifti():
    nifti_image = read_nifti_image(sample_nifti_file_path)
    nifti_image_as_np = extract_np_array_from_nifti_image(nifti_image)
    result = convert_dicom_np_ndarray_to_nifti_image(nifti_image_as_np)
    assert isinstance(result, nibabel.nifti1.Nifti1Image)
