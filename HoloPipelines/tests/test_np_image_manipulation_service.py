import numpy as np

from core.services import np_image_manipulation


def create_np_array(x_length, y_length, z_length):
    return np.random.randint(10, size=(x_length, y_length, z_length))


def test_crop_around_centre():
    image = create_np_array(20, 20, 20)
    cropped_image = np_image_manipulation.crop_around_centre(image, 10, 10, 10)
    assert cropped_image.shape == (10, 10, 10)


def test_downscale_and_conditionally_crop_with_only_downscale():
    image = create_np_array(32, 32, 16)
    downscaled_image = np_image_manipulation.downscale_and_conditionally_crop(image, 16)
    assert downscaled_image.shape == (16, 16, 8)


def test_downscale_and_conditionally_crop_with_downscale_and_crop():
    image = create_np_array(32, 32, 17)
    downscaled_and_cropped_image = np_image_manipulation.downscale_and_conditionally_crop(
        image, 16
    )
    assert downscaled_and_cropped_image.shape == (16, 16, 8)


def test_downscale_and_conditionally_crop_with_only_crop():
    image = create_np_array(32, 32, 17)
    cropped_image = np_image_manipulation.downscale_and_conditionally_crop(image, 32)
    assert cropped_image.shape == (32, 32, 16)
