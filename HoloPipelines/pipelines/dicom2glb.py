from components import dicom2numpy
from components import numpy2obj
from components import obj2gltfWrapper
import pathlib
import sys

dicomPath = pathlib.Path.cwd().joinpath("medicalScans", "dicom")
argCount = len(sys.argv)

if argCount != 3:
	print("Invalid number of argument")
	exit()

dicomData = sys.argv[1]
threshold = sys.argv[2]

tempNpy = dicom2numpy.main(str(dicomPath.joinpath(dicomData)), dicomData)
numpy2obj.main(tempNpy, threshold, dicomData)
obj2gltfWrapper.main(dicomData + ".obj", True)
print("dicom2glb: done")