from pathlib import Path

from pipelines.wrappers.obj2gltf import call_obj2gltf


# TODO: Needs refactoring! Why str and Path?
def convert_obj_to_glb_and_write(input_obj_path: Path, output_glb_path: str):
    return call_obj2gltf(input_obj_path, output_glb_path)
