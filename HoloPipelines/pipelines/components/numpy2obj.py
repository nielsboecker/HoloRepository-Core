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
import pathlib

nib.Nifti1Header.quaternion_threshold = -1e-06

cwd = pathlib.Path.cwd()

objPath = cwd.joinpath("output", "OBJ")
numpyPath = cwd.joinpath("numpy")


def make_mesh(image, threshold=300, step_size=1):
	print ("Transposing surface...")
	#print(image)
	if len(image.shape) == 5:
		image = image[:, :, :, 0, 0]
	p = image.transpose(2,1,0)#*******************************************************
	print(image.shape)
	#p = image.T
	
	print ("Calculating surface...")
	verts, faces, norm, val = measure.marching_cubes_lewiner(p, threshold, step_size=step_size, allow_degenerate=True) 
	return verts, faces, norm

def makeObj(fPath, thisThreshold, objOutput):
	if str(type(fPath)) == "<class 'numpy.ndarray'>":
		tempnumpy = fPath
	else:
		try:
			tempnumpy = np.load(str(numpyPath.joinpath(fPath)))
		except:
			print("Something went wrong with the numpy loading process, exiting...")
			exit()

	v, f, n = make_mesh(tempnumpy, float(thisThreshold), 1)#350


	f=f+1#not sure why we need this. the mesh looks 'weird' without it      solution ref >>>>>>   https://stackoverflow.com/questions/48844778/create-a-obj-file-from-3d-array-in-python      18/06/19

	newObj = open(str(objPath.joinpath('%s.obj' % objOutput)), 'w')
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
	print("component can't run on its own")



