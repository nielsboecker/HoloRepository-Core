#dicom2nifti > lungSegment > nifti2glb(pipeline)
#THERE IS THIS PROBLEM THAT DCM2NIFTI SAVES USING STUFF FROM DICOM META
import dcm2nifti
import components.lungSegment.main as lungSegment
import nifti2glb0 as nifti2glb
import fileHandler

slash = fileHandler.slash

def main(fname):
	dcm2nifti.main(str(fname))
	lungSegment.main(fname + ".nii.gz")
	#then del .nii.gz file and other segmented stuff ?
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
	dcm2nifti.main(str(fname))
	lungSegment.main(fname + ".nii.gz")
	#then del .nii.gz file and other segmented stuff ?
	nifti2glb.main("components" + slash + "lungSegment" + slash + "result" + slash + "sample_lung.nii.gz", 0.5)
	#pipeline has a return code?
	#outout file nameing
	#have a component just for saving files? (put file in temp folder first then call the save comp to sort it and name it)
	print("lungDicom2glb: done")