#todo return the file then del?
import dicom2nifti
import pydicom
from components import fileHandler as fileHand
#import dicom2nifti.settings as settings

dicomPath = fileHand.dicomPath
slash = fileHand.slash
niftiPath = fileHand.niftiPath

'''settings.disable_validate_slice_increment()
settings.enable_resampling()
settings.set_resample_spline_interpolation_order(1)
settings.set_resample_padding(-1000)'''

def main(fname):
	pydicom.decompress(dicomPath + fname + slash)
	dicom2nifti.convert_directory(dicomPath + fname + slash, niftiPath)#, reorient_nifti=True)
	print("nifti generated")

if __name__ == '__main__':
	import sys
	pydicom.decompress(dicomPath + sys.argv[1] + slash)
	#dicom2nifti.convert_directory(dicomPath + sys.argv[1] + slash, niftiPath)
	dicom2nifti.convert_directory(dicomPath + sys.argv[1] + slash, niftiPath, compression=True, reorient=True)
	print("dcm2nifti: done")
	#dicom2nifti.convert_directory(dicomPath + str(sys.argv[1], niftiPath, reorient=True)