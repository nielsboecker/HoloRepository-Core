import numpy as np
import nibabel as nib
from skimage import measure
import logging

logging.basicConfig(level=logging.INFO)
nib.Nifti1Header.quaternion_threshold = -1e-06


def generate_mesh(image_data: np.ndarray, threshold=300, step_size=1):
    logging.info("Transposing surface...")
    if (
            len(image_data.shape) == 5
    ):  # for nifti with 5D shape (time etc.), most nifti comes in 3D
        image_data = image_data[:, :, :, 0, 0]
    p = image_data.transpose((2, 1, 0))

    logging.info("Calculating surface...")
    verts, faces, norm, val = measure.marching_cubes_lewiner(
        p, threshold, step_size=step_size, allow_degenerate=True
    )
    return verts, faces, norm
