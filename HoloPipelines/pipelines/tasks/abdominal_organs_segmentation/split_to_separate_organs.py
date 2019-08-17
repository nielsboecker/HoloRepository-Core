# this comp generate numpy lists list from unique value from the numpy list input (comp exclusive for abdomen model at the moment)

# TODO: Depending on how we deciide for this pipeline, this component may get removed.
# Otherwise, separate organs need to be merged again!

import pathlib
from pipelines.components import compNumpy2obj as makeObj
from pipelines.wrappers.obj2gltf import convert_obj_to_glb
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)


def split_to_separate_organs(originalNumpy, outputPath):
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
                threshold=0,
                outputPath=pathlib.Path.cwd().joinpath("temp" + str(integer) + ".obj"),
            )
            convert_obj_to_glb(
                pathlib.Path.cwd().joinpath("temp" + str(integer) + ".obj"),
                outputPath.joinpath("organNo" + str(integer) + ".glb"),
                deleteOriginalObj=True,
            )
            outputGlbPathList.append(
                str(outputPath.joinpath("organNo" + str(integer) + ".glb"))
            )
    return outputGlbPathList
