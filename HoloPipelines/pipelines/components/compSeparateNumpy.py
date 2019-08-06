# this comp generate numpy lists list from unique value from the numpy list input (comp exclusive for abdomen model at the moment)

import pathlib
from components import compNumpy2obj as makeObj
from components import compObj2glbWrapper as makeGlb
import numpy as np
import sys
import logging


def main(inputNumpy, outputPath):
    outputPath = pathlib.Path(outputPath)
    # load numpy
    if isinstance(inputNumpy, np.ndarray):
        originalNumpy = inputNumpy
    else:
        try:
            # if inputNumpy is path to npy file
            originalNumpy = np.load(str(pathlib.Path(inputNumpy)))
        except Exception:
            sys.exit(
                "getMultipleNumpy: error occured while loading numpy. Please make sure the path to numpy is correct."
            )

    # get frequency. Maybe can add clustering later?
    unique, counts = np.unique(originalNumpy, return_counts=True)

    logging.info(np.asarray(unique))
    logging.info(np.asarray((unique, counts)).T)

    outputGlbPathList = []

    for integer in unique:
        if integer != 0:
            singleHUnumpy = originalNumpy == integer
            singleHUnumpy = singleHUnumpy.astype(int)
            makeObj.main(
                singleHUnumpy,
                0,
                pathlib.Path.cwd().joinpath("temp" + str(integer) + ".obj"),
            )
            makeGlb.main(  # need to change temp to dicom folder name
                pathlib.Path.cwd().joinpath("temp" + str(integer) + ".obj"),
                outputPath.joinpath("organNo" + str(integer) + ".glb"),
                True,
            )
            outputGlbPathList.append(
                str(outputPath.joinpath("organNo" + str(integer) + ".glb"))
            )
    return outputGlbPathList


if __name__ == "__main__":
    print("component can't run on its own")
