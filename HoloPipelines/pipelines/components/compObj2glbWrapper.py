import subprocess
import pathlib
from shutil import move
import os
import sys
import logging

newCwd = str(pathlib.Path(str(os.path.dirname(os.path.realpath(__file__)))))

success = True


def main(input_obj_path, output_glb_path, delete_original_obj=True, compress_glb=False):
    success = subprocess.run(
        ["obj2gltf", "-i", str(pathlib.Path(input_obj_path)), "-b"]
    )
    if success.returncode == 0:

        outputGlbPath = str(pathlib.Path(output_glb_path))
        move(str(pathlib.Path(input_obj_path)).replace(".obj", ".glb"), outputGlbPath)
        if delete_original_obj:
            os.remove(str(pathlib.Path(input_obj_path)))
        logging.info("obj2glb: conversion complete")

        # Draco compression. note that draco compresssion in viewers may not be common
        if compress_glb:
            success = subprocess.run(
                "gltf-pipeline",
                "-i",
                outputGlbPath,
                "-o",
                outputGlbPath,
                "-d",
                cwd=newCwd,
            )
            if success.returncode == 0:
                logging.info("obj2glb: Draco compression finished")
            else:
                sys.exit("obj2glb: Draco compression failed")
    else:
        sys.exit("obj2glb: conversion failed")
    logging.info("obj2glb: done")
    return outputGlbPath


if __name__ == "__main__":
    logging.info("component can't run on its own")
