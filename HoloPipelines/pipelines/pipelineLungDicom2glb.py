#NOTE: lungSegment will always output as sample_lung.nii.gz etc
from components import compDcm2nifti
#import components.compLungSegment.main
from components.lungSegment.main import main as lungSegment
from components import compNifti2numpy
from components import compNumpy2obj
from components import compObj2gltfWrapper
import pathlib
import sys
import os

def main(dicomPath, outputGlbPath):#TODO: update json
	generatedNiftiPath = compDcm2nifti.main(str(dicomPath), str(pathlib.Path.cwd().joinpath("medicalScans", "nifti", str(pathlib.PurePath(dicomPath).parts[-1]))))#convert dcm and move to temp path inside nifti folder. nifti will be in a sub folder named after the input dicom folder
	generatedSegmentedLungsNiftiPath = lungSegment(generatedNiftiPath)
	generatedNumpyList = compNifti2numpy.main(str(pathlib.Path(generatedSegmentedLungsNiftiPath)))
	generatedObjPath = compNumpy2obj.main(generatedNumpyList, 0.5, str(pathlib.Path.cwd().joinpath("output", "OBJ", "nifti2glb_tempObj.obj")))
	generatedGlbPath = compObj2gltfWrapper.main(generatedObjPath, str(pathlib.Path(outputGlbPath)), True, False)
	print("lungDicom2glb: done")

if __name__ == "__main__":
	main(str(sys.argv[1]), str(sys.argv[2]))