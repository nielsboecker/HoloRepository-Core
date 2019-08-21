import logging
import subprocess


def call_obj2gltf(obj_input_path: str, glb_output_path: str):
    obj2gltf_command = [
        "obj2gltf",
        "--binary",
        "--input",
        obj_input_path,
        "--output",
        glb_output_path,
    ]

    completed_process = subprocess.run(obj2gltf_command)
    if completed_process.returncode == 0:
        logging.info("obj2gltf wrapper: Conversion succeeded")
    else:
        raise Exception("obj2gltf wrapper: Conversion failed")
