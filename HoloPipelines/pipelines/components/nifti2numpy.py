import numpy as np
import nibabel as nib
from nilearn.image import resample_img
import scipy
from components import fileHandler
import platform

cwd = fileHandler.cwd
slash = fileHandler.slash

numpyPath = cwd + "numpys" + slash
niftiPath = cwd + "imgs" + slash + "nifti" + slash
numpyPath = cwd + "numpys" + slash

fName = ""
tempPath = ""

def getIO():
	if niftiPath[-3:] == ".gz":
		fName = fileHandler.getFname(".nii.gz", niftiPath)
	else:
		fName = fileHandler.getFname(".nii", niftiPath)
	tempPath = niftiPath + fName
	return [tempPath, fName]

def resample(dataPath, new_spacing=[1,1,1]):
	image = dataPath
	originalShape = image.shape
	header = image.header
	image._affline = None
	spacing = map(float, ([list(image.header.get_zooms())[2]] + [list(image.header.get_zooms())[0], list(image.header.get_zooms())[1]]))
	spacing = np.array(list(spacing))

	resize_factor = spacing / new_spacing
	new_real_shape = image.shape * resize_factor
	new_shape = np.round(new_real_shape)
	real_resize_factor = new_shape / image.shape
	new_spacing = spacing / real_resize_factor
	
	print ("Shape before resampling\t", originalShape)
	print ("Shape after resampling\t", image.shape)
	
	return image, new_spacing

def main(mainPath=tempPath, tempFname=fName, option=0):
	#https://github.com/nipy/nibabel/issues/626
	nib.Nifti1Header.quaternion_threshold = -1e-06
	img = nib.load(mainPath)

	img, newSpacing = resample(img)

	a = np.array(img.dataobj)
	if option == 1:
		np.save(numpyPath + "%s.npy" % tempFname[:-4], a)
		return 0
	return a

if __name__ == '__main__':
	lsIO = getIO()
	temp = main(lsIO[0], lsIO[1], 1)
	print(lsIO[1][:-4] + ".npy generated.")