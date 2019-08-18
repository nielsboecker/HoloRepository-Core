import logging
import nibabel
import numpy as np


def extract_np_array_from_nifti_image(image_data: nibabel.nifti1.Nifti1Image):
    """
    Returns the numpy array representation of the dataobj inside a NIfTI image
    :param image_data: NIfTI image
    :return: numpy array representing the image data
    """
    return np.array(image_data.dataobj)


def normalise_nifti_image(image_data: nibabel.nifti1.Nifti1Image):
    """
    After loading a NIfTI file, this function resamples it according to the file headers
    in order to compensate different slice thickness.
    :param image_data: input image data
    :return: normalised NIfTI
    """
    # TODO: Why copy??
    image = image_data
    # TODO: does the Nifti1Image have a .shape field? according to documentary, no?
    original_shape = image.shape[:3]

    # TODO: document what happens here
    # TODO: _affline seems like a typo and even as "affine" i don't see what it should do?
    image._affline = None
    spacing = map(
        float,
        (
                [list(image.header.get_zooms())[2]]
                + [list(image.header.get_zooms())[0], list(image.header.get_zooms())[1]]
        ),
    )
    spacing = np.array(list(spacing))

    new_spacing = [1, 1, 1]
    resize_factor = spacing / new_spacing
    new_real_shape = image.shape[:3] * resize_factor
    new_shape = np.round(new_real_shape)
    real_resize_factor = new_shape / image.shape[:3]
    # TODO: Why overriding variable? And also why is it unused anyway, afterwards?
    new_spacing = spacing / real_resize_factor

    logging.info("Shape before resampling\t" + repr(original_shape))
    logging.info("Shape after resampling\t" + repr(image.shape[:3]))

    # TODO: Is the image even changed??
    return image


def read_nifty_image(input_path: str):
    """
    Reads NIfTI image from disk.
    :param input_path: Path to the NIfTI image
    :return: NIfTI image represented as nibabel.nifti1.Nifti1Image
    """
    # Note: Workaround according to https://github.com/nipy/nibabel/issues/626
    nibabel.Nifti1Header.quaternion_threshold = -1e-06
    return nibabel.load(input_path)


def read_nifti_as_np_array_and_normalise(input_path: str):
    nifti_image: nibabel.nifti1.Nifti1Image = read_nifty_image(input_path)
    normalised_nifty_image: nibabel.nifti1.Nifti1Image = normalise_nifti_image(nifti_image)
    normalised_nifty_image_as_np_array: np.array = extract_np_array_from_nifti_image(normalised_nifty_image)
    return normalised_nifty_image_as_np_array
