from core.adapters.dicom_file import (
    read_dicom_dataset,
    read_dicom_pixels_as_np_ndarray,
    flip_numpy_array_dimensions,
    normalise_dicom,
    read_dicom_as_np_ndarray_and_normalise,
)

sample_dicom_directory_path = "./tests/utils/sample_dicom"


def test_read_dicom_dataset():
    result = read_dicom_dataset(sample_dicom_directory_path)
    assert len(result) == 4


def test_read_dicom_pixels_as_np_ndarray():
    result = read_dicom_pixels_as_np_ndarray(sample_dicom_directory_path)
    assert result.shape == (512, 512, 4)


def test_normalise_dicom():
    dicom_as_np_array = read_dicom_pixels_as_np_ndarray(sample_dicom_directory_path)
    result = normalise_dicom(dicom_as_np_array, sample_dicom_directory_path)
    assert result.shape == (256, 302, 2)


def test_flip_numpy_array_dimensions():
    dicom_as_np_array = read_dicom_pixels_as_np_ndarray(sample_dicom_directory_path)
    result = flip_numpy_array_dimensions(dicom_as_np_array)
    assert result.shape == (4, 512, 512)


def test_read_dicom_as_np_ndarray_and_normalise():
    result = read_dicom_as_np_ndarray_and_normalise(sample_dicom_directory_path)
    assert result.shape == (256, 302, 2)
