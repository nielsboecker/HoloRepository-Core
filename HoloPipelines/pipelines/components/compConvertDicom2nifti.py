import numpy as np
import nibabel as nib
import logging


def main(np_array):
    img = nib.Nifti1Image(np_array, np.eye(4))
    img.to_filename("test.nii.gz")


if __name__ == "__main__":
    logging.info("component can't run on its own")
