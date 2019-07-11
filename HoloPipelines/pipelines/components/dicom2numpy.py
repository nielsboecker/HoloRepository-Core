import numpy as np
import pydicom as dicom
import pydicom.pixel_data_handlers.gdcm_handler
import os
from glob import glob
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import scipy.ndimage
import pathlib
import time

cwd = pathlib.Path.cwd()
numpyPath = cwd.joinpath("numpy")

def load_scan(scanPath): #default was samples from dicom
	slices = [dicom.read_file(str(pathlib.Path(scanPath, s))) for s in os.listdir(str(scanPath))]
	slices.sort(key = lambda x: int(x.InstanceNumber))
	try:
		slice_thickness = np.abs(slices[0].ImagePositionscan[2] - slices[1].ImagePositionscan[2])
	except:
		slice_thickness = np.abs(slices[0].SliceLocation - slices[1].SliceLocation)
		
	for s in slices:
		s.SliceThickness = slice_thickness
		
	return slices


def get_pixels_hu(scans):
	image = np.stack([s.pixel_array for s in scans])
	image = image.astype(np.int16)

	image[image == -2000] = 0
	
	intercept = scans[0].RescaleIntercept
	slope = scans[0].RescaleSlope
	
	if slope != 1:
		image = slope * image.astype(np.float64)
		image = image.astype(np.int16)
		
	image += np.int16(intercept)
	
	return np.array(image, dtype=np.int16)




def resample(dataPath, new_spacing=[1,1,1]):#default to dataPath was samples from dicom
	scan = load_scan(dataPath)
	image = get_pixels_hu(scan)
	print ("Shape before resampling\t", image.shape)
	#TODO: add timer
	start = time.clock()
	# Determine current pixel spacing
	try:
		spacing = map(float, ([scan[0].SliceThickness] + [scan[0].PixelSpacing[0], scan[0].PixelSpacing[1]]))
		spacing = np.array(list(spacing))
	except:
		print(len(scan[0].PixelSpacing))
		print ("Pixel Spacing (row, col): (%f, %f) " % (scan[0].PixelSpacing[0], scan[0].PixelSpacing[1]))
		print("dicom2numpy: error loading scan")
		exit()

	resize_factor = spacing / new_spacing
	new_real_shape = image.shape * resize_factor
	new_shape = np.round(new_real_shape)
	real_resize_factor = new_shape / image.shape
	new_spacing = spacing / real_resize_factor
	
	image = scipy.ndimage.interpolation.zoom(image, real_resize_factor)
	print ("Resample done in:  " + str(time.clock()-start))
	print ("Shape after resampling\t", image.shape)
	
	return image, new_spacing

def main(inputPath, mainFname="samples", option=0):#default to inputPath was samples from dicom
	print("dicom2numpy: resampling dicom...")
	imgs_after_resamp, spacing = resample(inputPath)
	print("dicom2numpy: resampling done")
	if option == 1:
		np.save(str(numpyPath.joinpath("%s.npy" % mainFname)), imgs_after_resamp)
		return 0
	return imgs_after_resamp

if __name__ == '__main__':
	print("component can't be run on its own")


