import nifti2numpy
import numpy2obj
import fileHandler
import sys

slash = fileHandler.slash
argCount = len(sys.argv)

if argCount != 3:#need changing
	print("Invalid number of argument.")
	exit()

niftiData = sys.argv[1]
threshold = sys.argv[2]

#pipeline should actually deal with data retrieval, not giving the path to them components 
tempNpy = nifti2numpy.main(fileHandler.niftiPath + fileHandler.slash + fname, fname)
numpy2obj.main(tempNpy, threshold)
print("Task finished")