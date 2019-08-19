# this pipeline may be removed in the future as obj is not used to display 3D model on hololens
import logging
import pathlib

from core.adapters.nifti_file import read_nifti_as_np_array_and_normalise
from core.adapters.obj_file import write_mesh_as_obj
from core.services.marching_cubes import generate_mesh


def main(inputNiftiPath, outputObjPath, threshold, flipNpy=False):
    nifti_image_as_np_array = read_nifti_as_np_array_and_normalise(
        str(pathlib.Path(inputNiftiPath))
    )
    obj_output_path = pathlib.Path(outputObjPath)
    verts, faces, norm = generate_mesh(nifti_image_as_np_array, threshold)
    write_mesh_as_obj(verts, faces, norm, obj_output_path)

    logging.info("nifti2obj: done, obj saved to {}".format(obj_output_path))
