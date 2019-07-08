from components import nifti2numpy
from components import numpy2obj
from components import obj2gltfWrapper
from components import fileHandler
import sys

def main(fname, threshold):
	tempNii = fname.replace(".nii.gz", "").replace(".nii", "")
	tempNpy = nifti2numpy.main(fileHandler.niftiPath + fname, fname)
	numpy2obj.main(tempNpy, threshold, tempNii)
	obj2gltfWrapper.main(tempNii + ".obj", True)
	print("nifti2glb: done")

if __name__ == '__main__':
	import sys

	slash = fileHandler.slash
	argCount = len(sys.argv)

	if argCount != 3:
		print("Invalid number of argument")
		exit()

	niftiData = sys.argv[1]
	threshold = sys.argv[2]

	tempNii = niftiData.replace(".nii.gz", "").replace(".nii", "")

	tempNpy = nifti2numpy.main(fileHandler.niftiPath + niftiData, niftiData)
	numpy2obj.main(tempNpy, threshold, tempNii)
	obj2gltfWrapper.main(tempNii + ".obj", True)
	print("nifti2glb: done")