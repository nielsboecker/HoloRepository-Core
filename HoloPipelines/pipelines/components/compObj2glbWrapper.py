import subprocess
import pathlib
from shutil import move
import os
import sys

new_cwd = str(pathlib.Path(str(os.path.dirname(os.path.realpath(__file__)))))

success = True


def main(input_obj_path, output_glb_path, delete_original_obj=True, compress_glb=False):
    success = subprocess.run(
        ["obj2gltf", "-i", str(pathlib.Path(input_obj_path)), "-b"]
    )
    if success.returncode == 0:

        output_glb_path = output_glb_path
        move(str(pathlib.Path(input_obj_path)).replace(".obj", ".glb"), output_glb_path)
        if delete_original_obj:
            os.remove(str(pathlib.Path(input_obj_path)))
        print("obj2glb: conversion complete")

        # Draco compression. note that draco compresssion in viewers may not be common
        if compress_glb:
            success = subprocess.run(
                "gltf-pipeline",
                "-i",
                output_glb_path,
                "-o",
                output_glb_path,
                "-d",
                cwd=new_cwd,
            )
            if success.returncode == 0:
                print("obj2glb: Draco compression finished")
            else:
                sys.exit("obj2glb: Draco compression failed")
    else:
        sys.exit("obj2glb: conversion failed")
    print("obj2glb: done")
    return output_glb_path


if __name__ == "__main__":
    print("component can't run on its own")
