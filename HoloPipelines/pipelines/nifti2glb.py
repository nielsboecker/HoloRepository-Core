#almost identical to nifti2obj, with an addition to the wrapper
#TODO: clean this up?

from components import nifti2numpy#this import stuff in the future will be dockerized
from components import numpy2obj
from components import obj2gltfWrapper

from components import fileHandler#you can stay?
import sys

def main(fname, threshold):

	#pipeline should actually deal with data retrieval, not giving the path to them components 
	tempNii = fname.replace(".nii.gz", "").replace(".nii", "")

	tempNpy = nifti2numpy.main(fileHandler.niftiPath + fname, fname)
	numpy2obj.main(tempNpy, threshold, tempNii)
	obj2gltfWrapper.main(tempNii + ".obj", True)
	print("nifti2glb: done")

if __name__ == '__main__':
	import sys

	slash = fileHandler.slash
	argCount = len(sys.argv)

	if argCount != 3:#need changing
		print("Invalid number of argument")
		exit()

	niftiData = sys.argv[1]
	threshold = sys.argv[2]

	#pipeline should actually deal with data retrieval, not giving the path to them components 
	tempNii = niftiData.replace(".nii.gz", "").replace(".nii", "")

	tempNpy = nifti2numpy.main(fileHandler.niftiPath + niftiData, niftiData)
	numpy2obj.main(tempNpy, threshold, tempNii)
	obj2gltfWrapper.main(tempNii + ".obj", True)
	print("nifti2glb: done")