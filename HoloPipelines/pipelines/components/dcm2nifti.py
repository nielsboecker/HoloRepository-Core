#todo return the file then del?
import dicom2nifti
import pathlib
#import dicom2nifti.settings as settings

dicomPath = pathlib.Path.cwd().joinpath("medicalScans", "dicom")
niftiPath = pathlib.Path.cwd().joinpath("medicalScans", "nifti")

def main(fname):
	dicom2nifti.convert_directory(str(dicomPath.joinpath(fname)), str(niftiPath))
	print("dcm2nifti: done")

if __name__ == '__main__':
	print("component can't run on its own")