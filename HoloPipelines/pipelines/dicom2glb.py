from components import dicom2numpy
from components import numpy2obj
from components import obj2gltfWrapper
import pathlib
import sys

dicomPath = pathlib.Path.cwd().joinpath("medicalScans", "dicom")

def main(dicomData, threshold):
	tempNpy = dicom2numpy.main(str(dicomPath.joinpath(dicomData)), dicomData)
	numpy2obj.main(tempNpy, threshold, dicomData)
	obj2gltfWrapper.main(dicomData + ".obj", True)
	print("dicom2glb: done")

if __name__ == "__main__":
	dicomData = sys.argv[1]
	threshold = sys.argv[2]

	main(dicomData, threshold)