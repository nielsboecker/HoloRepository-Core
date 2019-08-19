import logging

import numpy as np
from skimage import measure


def generate_mesh(image_data: np.ndarray, threshold=300, step_size=1):
    logging.info("Transposing surface...")
    # for nifti with 5D shape (time etc.), most nifti comes in 3D
    if len(image_data.shape) == 5:
        image_data = image_data[:, :, :, 0, 0]
    p = image_data.transpose((2, 1, 0))

    logging.info("Calculating surface...")
    verts, faces, norm, val = measure.marching_cubes_lewiner(
        p, threshold, step_size=step_size, allow_degenerate=True
    )
    return verts, faces, norm
