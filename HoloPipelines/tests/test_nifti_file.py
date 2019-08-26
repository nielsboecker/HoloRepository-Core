import pytest
import sys
import os
import requests
import nibabel
import numpy
import logging
from zipfile import ZipFile

sys.path.insert(1, os.path.join(sys.path[0], ".."))  # noqa
from core.adapters.nifti_file import (
    extract_np_array_from_nifti_image,
    extract_np_array_from_nifti_image_and_normalise,
    read_nifti_image,
    read_nifti_as_np_array,
    write_nifti_image,
    convert_dicom_np_ndarray_to_nifti_image,
)


test_input_path = "__test_input__"
nifti_directory_path = f"{test_input_path}/nifti"
sample_nifti_file = "1103_3_glm.nii"
sample_nifti_zipped_file = "__test_nifti__.nii.zip"
sample_output_nifti_file = "__test_nifti_output__.nii"


@pytest.fixture
def test_setup():
    if not os.path.exists(f"{nifti_directory_path}"):
        os.makedirs(f"{nifti_directory_path}")

    logging.info("Checking for sample files...")

    # download nifti sample data
    if not os.path.exists(f"{nifti_directory_path}/{sample_nifti_file}"):
        nifti_file_url = (
            "https://holoblob.blob.core.windows.net/test/1103_3_glm.nii.zip"
        )
        response = requests.get(nifti_file_url)
        open(f"{nifti_directory_path}/{sample_nifti_zipped_file}", "wb+").write(
            response.content
        )

        logging.info("Decompressing...")
        with ZipFile(
            f"{nifti_directory_path}/{sample_nifti_zipped_file}", "r"
        ) as zipObj:  # unzip nifti file
            zipObj.extractall(f"{nifti_directory_path}")
        os.remove(f"{nifti_directory_path}/{sample_nifti_zipped_file}")

    logging.info("setup: done")

    # delete output file if exists
    if os.path.exists(f"{nifti_directory_path}/{sample_output_nifti_file}"):
        os.remove(f"{nifti_directory_path}/{sample_output_nifti_file}")


# read nifti
def test_read_nifti(test_setup):
    nifti_image = read_nifti_image(f"{nifti_directory_path}/{sample_nifti_file}")
    assert isinstance(nifti_image, nibabel.nifti1.Nifti1Image)


# read nifti as numpy array
def test_read_nifti_as_np_array(test_setup):
    nifti_image = read_nifti_as_np_array(f"{nifti_directory_path}/{sample_nifti_file}")
    assert isinstance(nifti_image, numpy.ndarray)


# normalise nifti that is already normalised (so the shape has to be the same after rescaling)
def test_normalise_nifti(test_setup):
    nifti_image = read_nifti_image(f"{nifti_directory_path}/{sample_nifti_file}")
    nifti_image_as_np = extract_np_array_from_nifti_image(nifti_image)

    normalised_nifti_image_as_np = extract_np_array_from_nifti_image_and_normalise(
        nifti_image
    )
    assert normalised_nifti_image_as_np.shape == nifti_image_as_np.shape


# writing nifti file
def test_write_nifti(test_setup):
    nifti_image = read_nifti_image(f"{nifti_directory_path}/{sample_nifti_file}")
    write_nifti_image(nifti_image, f"{nifti_directory_path}/{sample_output_nifti_file}")
    assert os.path.exists(f"{nifti_directory_path}/{sample_output_nifti_file}")


# convert numpy array to nifti
def test_convert_np_to_nifti(test_setup):
    nifti_image = read_nifti_image(f"{nifti_directory_path}/{sample_nifti_file}")
    nifti_image_as_np = extract_np_array_from_nifti_image(nifti_image)
    nifti_image_from_np = convert_dicom_np_ndarray_to_nifti_image(nifti_image_as_np)
    assert isinstance(nifti_image_from_np, nibabel.nifti1.Nifti1Image)
