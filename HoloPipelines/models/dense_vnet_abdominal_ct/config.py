import nibabel as nib
import numpy as np
import configparser

CONFIG_PATH = "/root/niftynet/extensions/dense_vnet_abdominal_ct/config.ini"


def read_nifti_image(input_file_path: str) -> nib.nifti1.Nifti1Image:
    """
    Reads NIfTI image from disk.
    :param input_file_path: path to the NIfTI image
    :return: NIfTI image represented as nibabel.nifti1.Nifti1Image
    """
    # Note: Workaround according to https://github.com/nipy/nibabel/issues/626
    nib.Nifti1Header.quaternion_threshold = -1e-06
    return nib.load(input_file_path)


def get_nifti_resolution(image_data: nib.nifti1.Nifti1Image):
    """
    Returns the resolution from nifti image.
    :param image_data: NIfTI image
    :return: tuple of resolution (x, y, z)
    """
    return np.array(image_data.dataobj).shape[:3]


def update_config_with_new_resolution(input_file_path: str):
    """
    Update the resolution parameters in config.ini with the resolution from nifti image.
    :param input_file_path: path to the NIfTI image
    """
    nifti_image = read_nifti_image(input_file_path)
    nifti_shape = get_nifti_resolution(nifti_image)

    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)

    config.set("ct", "spatial_window_size", str(nifti_shape))

    with open(CONFIG_PATH, "w") as config_file:
        config.write(config_file)
