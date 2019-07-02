#where would this type of files go? (just gonna call them pipeline config for now)
#from DB(ref to diagram)?
#who's our target user? for pipeline dev

import nifti2numpy#this import stuff in the future will be dockerized
import numpy2obj

import fileHandler#you can stay?
import sys

slash = fileHandler.slash
argCount = len(sys.argv)

if argCount != 4:#need changing
	print("Invalid number of argument")
	exit()

niftiData = sys.argv[1]
threshold = sys.argv[2]
flipNpy = sys.argv[3]

#pipeline should actually deal with data retrieval, not giving the path to them components 
tempNpy = nifti2numpy.main(fileHandler.niftiPath + fileHandler.slash + niftiData, niftiData)
if flipNpy:
	tempNpy = np.flip(tempNpy, 0)
	tempNpy = np.flip(tempNpy, 1)
numpy2obj.main(tempNpy, threshold, "heyitsyaboi_nifti2obj_comdelmepls")
print("Task finished")