from components import nifti2numpy
from components import numpy2obj
from components import obj2gltfWrapper
from components import fileHandler
import sys

def main(fname, threshold, outputName=""):
	tempNii = fname.replace(".nii.gz", "").replace(".nii", "")
	tempNpy = nifti2numpy.main(fileHandler.niftiPath + fname, fname)
	if outputName != "":
		tempNii = outputName
	numpy2obj.main(tempNpy, threshold, "__temp__" + tempNii)
	obj2gltfWrapper.main("__temp__" + tempNii + ".obj", True)
	print("nifti2glb: done")

if __name__ == '__main__':
	import sys

	slash = fileHandler.slash
	argCount = len(sys.argv)

	if argCount != 3 and argCount != 4:
		print("Invalid number of argument")
		exit()

	niftiData = sys.argv[1]
	threshold = sys.argv[2]
	outputName = niftiData
	if argCount == 4:
		outputName = sys.argv[3]

	tempNii = niftiData.replace(".nii.gz", "").replace(".nii", "")

	tempNpy = nifti2numpy.main(fileHandler.niftiPath + niftiData, outputName)
	numpy2obj.main(tempNpy, threshold, tempNii)
	obj2gltfWrapper.main(tempNii + ".obj", True)
	print("nifti2glb: done")