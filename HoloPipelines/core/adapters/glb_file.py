from core.wrappers.obj2gltf import call_obj2gltf


def convert_obj_to_glb_and_write(input_obj_path: str, output_glb_path: str):
    call_obj2gltf(input_obj_path, output_glb_path)
