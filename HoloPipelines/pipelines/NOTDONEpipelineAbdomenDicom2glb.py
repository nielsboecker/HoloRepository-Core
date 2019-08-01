# ----this pl in a nutshell:
# dicom2nifti
# use the new http request comp to NN segment the nifti file
# nifti2numpy
# getMultipleNumpy
# numpy2obj
# obj2gltf
# GLB coloring time? ';) (pygltflib)

#TODO should i make a cleanup comp for all those temp obj and nifti?
from components import compDcm2nifti
from components import compJobStatus # here
from components import compNifti2numpy
from components import compNumpy2obj
from components import compObj2glbWrapper
from components import compCommonPath # I dont think this is here in API branch
import pathlib
import sys

def main(inputDicomPath, outputGlbPath):
	generatedNiftiFolderPath = compDcm2nifti.main(str(pathlib.Path(inputDicomPath)), str(compCommonPath.nifti.joinpath("PleaseLookAtThis")))
	segmentedNiftiPath = compJobStatus.main(generatedNiftiFolderPath, "PleaseLookAtThis")
	generatedNumpyList = compNifti2numpy.main(segmentedNiftiPath) # check args here pls
	# will need to update comp to take a list of numpy list as well as folder of numpy list?
	# and yeah will need to think of how i should return it
	# for each numpy list 
	#		generate obj >> conv to glb >> color
	# but would that kinda make pl a bit messy?
	# should i just let comp handle it in a case that it gets a list of stuff?

if __name__ == "__main__":
	main()# add sys.argv[] here