import numpy as np
import nibabel as nib
from nilearn.image import resample_img
import scipy
import pathlib
import platform

cwd = pathlib.Path.cwd()

numpyPath = cwd.joinpath("numpy")

fName = ""
tempPath = ""

def resample(dataPath, new_spacing=[1,1,1]):
	image = dataPath
	originalShape = image.shape[:3]
	header = image.header
	image._affline = None
	spacing = map(float, ([list(image.header.get_zooms())[2]] + [list(image.header.get_zooms())[0], list(image.header.get_zooms())[1]]))
	spacing = np.array(list(spacing))

	resize_factor = spacing / new_spacing
	new_real_shape = image.shape[:3] * resize_factor
	new_shape = np.round(new_real_shape)
	real_resize_factor = new_shape / image.shape[:3]
	new_spacing = spacing / real_resize_factor
	
	print ("Shape before resampling\t", originalShape)
	print ("Shape after resampling\t", image.shape[:3])
	
	return image, new_spacing

def main(inputNiftiPath, outputNumpyPath=""):
	#https://github.com/nipy/nibabel/issues/626
	nib.Nifti1Header.quaternion_threshold = -1e-06
	img = nib.load(inputNiftiPath)

	img, newSpacing = resample(img)

	numpyList = np.array(img.dataobj)
	if str(outputNumpyPath) != "":
		outputNumpyPath = str(pathlib.Path(outputNumpyPath))
		np.save(str(pathlib.Path(outputNumpyPath)), numpyList)
	return numpyList

if __name__ == '__main__':
	print("component can't run on its own")