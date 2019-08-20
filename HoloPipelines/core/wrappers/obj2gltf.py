import logging
import os
import pathlib
import subprocess
import sys

new_cwd = str(pathlib.Path(str(os.path.dirname(os.path.realpath(__file__)))))

success = True


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
        logging.info("obj2glb: conversion complete")
    else:
        sys.exit("obj2glb: conversion failed")

    logging.info("obj2glb: done")
    return glb_output_path
