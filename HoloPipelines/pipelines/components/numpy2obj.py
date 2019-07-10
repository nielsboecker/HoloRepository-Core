import numpy as np
import nibabel as nib
import pydicom as dicom
import pydicom.pixel_data_handlers.gdcm_handler
import os
import time
import matplotlib.pyplot as plt
from glob import glob
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import scipy.ndimage
from skimage import morphology
from skimage import measure
from skimage.transform import resize
from sklearn.cluster import KMeans
from components import fileHandler

nib.Nifti1Header.quaternion_threshold = -1e-06

slash = fileHandler.slash
cwd = os.getcwd() + slash

imgPath = cwd + "imgs" + slash
objPath = fileHandler.objPath
outputPath = cwd + "outputs" + slash
numpyPath = cwd + "numpys" + slash


def make_mesh(image, threshold=300, step_size=1):
	print ("Transposing surface...")
	p = image.transpose(2,1,0)
	
	print ("Calculating surface...")
	verts, faces, norm, val = measure.marching_cubes_lewiner(p, threshold, step_size=step_size, allow_degenerate=True) 
	return verts, faces, norm

def getIO():
	fName = fileHandler.getFname(".npy", numpyPath)
	tempPath = fileHandler.dicomPath + str(fName) + slash
	thresholdinput = input("Please enter HU threshold(int):  ")
	return [tempPath, fName, thresholdinput]

def makeObj(fPath, thisThreshold, objOutput):
	if str(type(fPath)) == "<class 'numpy.ndarray'>":
		tempnumpy = fPath
	else:
		try:
			tempnumpy = np.load(numpyPath + fPath)
		except:
			print("Something went wrong with the numpy loading process, exiting...")
			exit()

	v, f, n = make_mesh(tempnumpy, float(thisThreshold), 1)#350


	f=f+1#not sure why we need this. the mesh looks 'weird' without it      solution ref >>>>>>   https://stackoverflow.com/questions/48844778/create-a-obj-file-from-3d-array-in-python      18/06/19

	newObj = open(objPath + '%s.obj' % objOutput, 'w')
	for item in v:
		newObj.write("v {0} {1} {2}\n".format(item[0],item[1],item[2]))

	for item in n:
		newObj.write("vn {0} {1} {2}\n".format(item[0],item[1],item[2]))

	for item in f:
		newObj.write("f {0}//{0} {1}//{1} {2}//{2}\n".format(item[0],item[1],item[2]))  
	newObj.close()


def main(mainFchoice, mainThreshold):
	makeObj(mainFchoice, mainThreshold)
	print ("numpy2obj: done")

def main(mainFchoice, mainThreshold, outputName):
	makeObj(mainFchoice, mainThreshold, outputName)
	print ("numpy2obj: done")

if __name__ == '__main__':
	lsIO = getIO()
	tempInput = input("Please enter name for 'obj' file(without .obj extension), or leave blank for the same name as .npy:  ")
	if str(tempInput) == "":
		tempInput = lsIO[1]
	main(lsIO[1], lsIO[2], tempInput)
	print ("numpy2obj: done")



