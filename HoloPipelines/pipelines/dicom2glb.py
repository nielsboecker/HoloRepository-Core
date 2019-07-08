import os
from components import dicom2numpy
from components import numpy2obj
from components import obj2gltfWrapper
from components import fileHandler
import sys

slash = fileHandler.slash
argCount = len(sys.argv)

if argCount != 3:
	print("Invalid number of argument")
	exit()

dicomData = sys.argv[1]
threshold = sys.argv[2]

tempNpy = dicom2numpy.main(fileHandler.dicomPath + dicomData + fileHandler.slash, dicomData)
numpy2obj.main(tempNpy, threshold, dicomData)
obj2gltfWrapper.main(dicomData + ".obj", True)
print("dicom2glb: done")