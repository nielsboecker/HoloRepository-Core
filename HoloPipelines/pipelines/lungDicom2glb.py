#dicom2nifti > lungSegment > nifti2glb(pipeline)
#THERE IS THIS PROBLEM THAT DCM2NIFTI SAVES USING STUFF FROM DICOM META
#TODO this pipeline will always save as sample_lung.glb as it gets its nii from lungSegment
from components import dcm2nifti
import components.lungSegment.main as lungSegment
import nifti2glb as nifti2glb
from components import fileHandler
import subprocess

slash = fileHandler.slash

def main(fname):
	dcm2nifti.main(str(fname))
	lungSegment.main(lower(str(fname)) + ".nii.gz")
	#then del .nii.gz file and other segmented stuff ?
	sucess = subprocess.run(["mv", str("pipelines" + slash + "components" + slash + "lungSegment" + slash + "result" + slash + "sample_lung.nii.gz"), fileHandler.niftiPath])
	#success = subprocess.run(["rm", str(objPath + fname)])
	nifti2glb.main("components" + slash + "lungSegment" + slash + "result" + slash + "sample_lung.nii.gz", 0.5)
	#pipeline has a return code?
	#outout file nameing
	#have a component just for saving files? (put file in temp folder first then call the save comp to sort it and name it)
	print("lungDicom2glb: done")

if __name__ == "__main__":
	import sys
	if len(sys.argv) != 2:
		"lungDicom2glb: invalid number of argument"
		exit()
	fname = str(sys.argv[1])
	#sucess = subprocess.run(["mv", str(fileHandler.cwd + "pipelines" + slash + "components" + slash + "lungSegment" + slash + "result" + slash + "sample_lung.nii.gz"), fileHandler.niftiPath])
	dcm2nifti.main(str(fname))
	lungSegment.main(fname + ".nii.gz")
	sucess = subprocess.run(["mv", str(fileHandler.cwd + "pipelines" + slash + "components" + slash + "lungSegment" + slash + "result" + slash + "sample_lung.nii.gz"), fileHandler.niftiPath])
	#then del .nii.gz file and other segmented stuff ?
	nifti2glb.main("sample_lung.nii.gz", 0.5)
	success = subprocess.run(["rm", str(fileHandler.niftiPath + "sample_lung.nii.gz")])
	#pipeline has a return code?
	#outout file nameing
	#have a component just for saving files? (put file in temp folder first then call the save comp to sort it and name it)
	print("lungDicom2glb: done")