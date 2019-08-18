from pathlib import Path

from pipelines.wrappers.obj2gltf import call_obj2gltf


def convert_obj_to_glb_and_write(input_obj_path: Path, output_glb_path: Path):
    return call_obj2gltf(input_obj_path, output_glb_path)
