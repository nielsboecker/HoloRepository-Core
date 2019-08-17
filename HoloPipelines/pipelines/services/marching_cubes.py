import numpy as np
import nibabel as nib
from skimage import measure
import pathlib
import sys
import logging

logging.basicConfig(level=logging.INFO)
nib.Nifti1Header.quaternion_threshold = -1e-06


def generate_mesh(image, threshold=300, step_size=1):
    logging.info("Transposing surface...")
    if (
        len(image.shape) == 5
    ):  # for nifti with 5D shape (time etc.), most nifti comes in 3D
        image = image[:, :, :, 0, 0]
    p = image.transpose(2, 1, 0)

    logging.info("Calculating surface...")
    verts, faces, norm, val = measure.marching_cubes_lewiner(
        p, threshold, step_size=step_size, allow_degenerate=True
    )
    return verts, faces, norm


def generate_obj(input_numpy, this_threshold, output_obj_path):
    if isinstance(input_numpy, np.ndarray):
        numpy_data = input_numpy
    else:
        try:
            numpy_data = np.load(str(pathlib.Path(input_numpy)))

        except Exception as e:
            sys.exit(
                "numpy2obj: error occured while loading numpy. Please make sure the path to numpy is correct. {}".format(
                    e
                )
            )

    verts, faces, norm = generate_mesh(numpy_data, float(this_threshold), 1)

    faces = (
        faces + 1
    )  # https://stackoverflow.com/questions/48844778/create-a-obj-file-from-3d-array-in-python      18/06/19

    newObj = open(str(pathlib.Path(output_obj_path)), "w")
    for item in verts:
        newObj.write("v {0} {1} {2}\n".format(item[0], item[1], item[2]))

    for item in norm:
        newObj.write("vn {0} {1} {2}\n".format(item[0], item[1], item[2]))

    for item in faces:
        newObj.write("f {0}//{0} {1}//{1} {2}//{2}\n".format(item[0], item[1], item[2]))
    newObj.close()
