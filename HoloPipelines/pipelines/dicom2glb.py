#TODO: clean this up?
import os
from components import dicom2numpy#this import stuff in the future will be dockerized
from components import numpy2obj
from components import obj2gltfWrapper
from components import fileHandler#you can stay?
import sys

slash = fileHandler.slash
argCount = len(sys.argv)

if argCount != 3:#need changing
	print("Invalid number of argument")
	exit()

dicomData = sys.argv[1]
threshold = sys.argv[2]

#pipeline should actually deal with data retrieval, not giving the path to them components 

tempNpy = dicom2numpy.main(fileHandler.dicomPath + dicomData + fileHandler.slash, dicomData)
numpy2obj.main(tempNpy, threshold, dicomData)
obj2gltfWrapper.main(dicomData + ".obj", True)
print("Task finished")