from core.adapters.dicom_file import (
    read_dicom_dataset,
    read_dicom_pixels_as_np_ndarray,
    flip_numpy_array_dimensions,
    normalise_dicom,
    read_dicom_as_np_ndarray_and_normalise,
)

input_dir = "./tests/utils/sample_dicom"
dicom_np_array = read_dicom_pixels_as_np_ndarray(input_dir)


def test_read_dicom_dataset():

    assert len(read_dicom_dataset(input_dir)) == 4


def test_read_dicom_pixels_as_np_ndarray():

    assert read_dicom_pixels_as_np_ndarray(input_dir).shape == (512, 512, 4)
    # assert mock.called


def test_flip_numpy_array_dimensions():

    assert len(flip_numpy_array_dimensions())


def test_normalise_dicom():

    assert normalise_dicom(dicom_np_array, input_dir).shape == (256, 302, 2)


def test_flip_numpy_array_dimensions():

    assert flip_numpy_array_dimensions(dicom_np_array).shape == (4, 512, 512)


def test_read_dicom_as_np_ndarray_and_normalise():

    assert read_dicom_as_np_ndarray_and_normalise(input_dir).shape == (256, 302, 2)
