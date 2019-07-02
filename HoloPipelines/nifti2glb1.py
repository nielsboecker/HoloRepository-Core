#almost identical to nifti2obj, with an addition to the wrapper

import nifti2numpy#this import stuff in the future will be dockerized
import numpy2obj
import obj2gltfWrapper

import fileHandler#you can stay?
import sys

slash = fileHandler.slash
argCount = len(sys.argv)

if argCount != 3:#need changing
	print("Invalid number of argument")
	exit()

niftiData = sys.argv[1]
threshold = sys.argv[2]

#pipeline should actually deal with data retrieval, not giving the path to them components 
tempNpy = nifti2numpy.main(fileHandler.niftiPath + niftiData, niftiData)
numpy2obj.main(tempNpy, threshold, niftiData.replace(".nii.gz", "").replace(".nii", ""))
obj2gltfWrapper.main(niftiData + ".obj", True)
print("Task finished")