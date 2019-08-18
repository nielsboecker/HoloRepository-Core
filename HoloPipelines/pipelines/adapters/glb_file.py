from pipelines.wrappers.obj2gltf import call_obj2gltf


def convert_obj_to_glb(input_obj_path: str, output_glb_path: str, compress_glb: bool = False):
    return call_obj2gltf(input_obj_path, output_glb_path, compress_glb)
