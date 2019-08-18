import logging

from pipelines.services.marching_cubes import generate_obj
from pipelines.wrappers.obj2gltf import call_obj2gltf


def convert_numpy_to_obj(input_data, main_threshold, output_path):
    generate_obj(input_data, main_threshold, output_path)
    logging.info("numpy2obj: done")
    return output_path


def convert_obj_to_glb(input_obj_path: str, output_glb_path: str, delete_original_obj: bool = True,
                       compress_glb: bool = False):
    return call_obj2gltf(input_obj_path, output_glb_path, delete_original_obj, compress_glb)
