#todo return the file then del?
import dicom2nifti
from components import fileHandler as fileHand
#import dicom2nifti.settings as settings

dicomPath = fileHand.dicomPath
slash = fileHand.slash
niftiPath = fileHand.niftiPath

def main(fname):
	dicom2nifti.convert_directory(dicomPath + fname + slash, niftiPath)
	print("dcm2nifti: done")

if __name__ == '__main__':
	import sys
	dicom2nifti.convert_directory(dicomPath + sys.argv[1] + slash, niftiPath)
	print("dcm2nifti: done")