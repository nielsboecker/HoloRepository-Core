import subprocess
import pathlib
from shutil import move
import os
import sys
import logging

logging.basicConfig(level=logging.INFO)
new_cwd = str(pathlib.Path(str(os.path.dirname(os.path.realpath(__file__)))))

success = True


def call_obj2gltf(input_obj_path, output_glb_path):
    success = subprocess.run(
        ["obj2gltf", "-i", str(pathlib.Path(input_obj_path)), "-b"]
    )
    if success.returncode == 0:

        output_glb_path = output_glb_path
        # TODO: Can this be nicer? Maybe a "-o" flag for obj2gltf
        move(str(pathlib.Path(input_obj_path)).replace(".obj", ".glb"), output_glb_path)
        logging.info("obj2glb: conversion complete")

    else:
        sys.exit("obj2glb: conversion failed")
    logging.info("obj2glb: done")
    return output_glb_path
