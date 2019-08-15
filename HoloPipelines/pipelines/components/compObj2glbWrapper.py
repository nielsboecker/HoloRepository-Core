import subprocess
import pathlib
from shutil import move
import os
import sys
import logging

logging.basicConfig(level=logging.INFO)
newCwd = str(pathlib.Path(str(os.path.dirname(os.path.realpath(__file__)))))

success = True


def main(inputObjPath, outputGlbPath, deleteOriginalObj=True, compressGlb=False):
    success = subprocess.run(["obj2gltf", "-i", str(pathlib.Path(inputObjPath)), "-b"])
    if success.returncode == 0:
        outputGlbPath = str(pathlib.Path(outputGlbPath))
        move(str(pathlib.Path(inputObjPath)).replace(".obj", ".glb"), outputGlbPath)
        if deleteOriginalObj:
            os.remove(str(pathlib.Path(inputObjPath)))
        logging.info("obj2glb: conversion complete")

        # Draco compression. note that draco compresssion in viewers may not be common
        if compressGlb:
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
    logging.error("component can't run on its own")
