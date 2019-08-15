# this comp generate numpy lists list from unique value from the numpy list input (comp exclusive for abdomen model at the moment)

import pathlib
from components import compNumpy2obj as makeObj
from components import compObj2glbWrapper as makeGlb
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)


def main(originalNumpy, outputPath):
    outputPath = pathlib.Path(outputPath)

    # get frequency
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
                mainThreshold=0,
                outputPath=pathlib.Path.cwd().joinpath("temp" + str(integer) + ".obj"),
            )
            makeGlb.main(
                pathlib.Path.cwd().joinpath("temp" + str(integer) + ".obj"),
                outputPath.joinpath("organNo" + str(integer) + ".glb"),
                deleteOriginalObj=True,
            )
            outputGlbPathList.append(
                str(outputPath.joinpath("organNo" + str(integer) + ".glb"))
            )
    return outputGlbPathList


if __name__ == "__main__":
    logging.error("component can't run on its own")
