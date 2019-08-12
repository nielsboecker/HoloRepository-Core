# TODO change file name cos i legit dont know what to name this. File naming is not the same to the rest of comp format anyway
# this basically generate numpy lists list (list 4 days boi) from unique value from the numpy list input

# will also need to update the imports here as i was running it on some alien directory
import pathlib
import dupeNifti2numpy as getNp
import dupeNumpy2obj as makeObj
import dupeObj2gltfWrapper as makeGlb
import numpy as np
import sys

# load numpy
originalNumpy = getNp.main(str(pathlib.Path(sys.argv[1])))

# get frequency. Maybe can add clustering later?
unique, counts = np.unique(originalNumpy, return_counts=True)

print(np.asarray(unique))
print("")
print(np.asarray((unique, counts)).T)

for integer in unique:
    if integer != 0:
        singleHUnumpy = originalNumpy == integer
        singleHUnumpy = singleHUnumpy.astype(int)
        makeObj.main(
            singleHUnumpy,
            0,
            pathlib.Path.cwd().joinpath("output", "temp" + str(integer) + ".obj"),
        )
        makeGlb.main(  # need to change temp to dicom folder name
            pathlib.Path.cwd().joinpath("output", "temp" + str(integer) + ".obj"),
            pathlib.Path.cwd().joinpath("output", "organNo" + str(integer) + ".glb"),
            True,
        )

# TODO gltf coloring time, actually nah that should be done in the pipeline


# TODO remove rest. I dont think we will be needing this anymore?

# a = [0 if a_ > thresh for a_ in a]
# x[x > .5] = .5
"""
    if flipNpy:#not sure if this function will be needed. likely to be removed later
        generatedNumpyList = np.flip(generatedNumpyList, 0)
        generatedNumpyList = np.flip(generatedNumpyList, 1)
        """
