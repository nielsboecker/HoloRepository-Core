#THERE IS THIS PROBLEM THAT DCM2NIFTI SAVES USING STUFF FROM DICOM META
#TODO this pipeline will always save as sample_lung.glb as it gets its nii from lungSegment
from components import dcm2nifti
import components.lungSegment.main as lungSegment
import nifti2glb as nifti2glb
import pathlib
import subprocess

cwd = pathlib.Path.cwd()
niftiPath = cwd.joinpath("medicalScans", "nifti")

def main(fname):
	dcm2nifti.main(str(fname))
	lungSegment.main(lower(str(fname)) + ".nii.gz")
	sucess = subprocess.run(["mv", str(cwd.joinpath("pipelines", "components", "lungSegment", "result", "sample_lung.nii.gz")), str(niftiPath)])
	nifti2glb.main(str(cwd.joinpath("components", "lungSegment", "result", "sample_lung.nii.gz")), 0.5)
	print("lungDicom2glb: done")

if __name__ == "__main__":
	import sys
	if len(sys.argv) != 2:
		"lungDicom2glb: invalid number of argument"
		exit()
	fname = str(sys.argv[1])
	dcm2nifti.main(str(fname))
	lungSegment.main(fname + ".nii.gz")
	sucess = subprocess.run(["mv", str(cwd.joinpath("pipelines", "components", "lungSegment", "result", "sample_lung.nii.gz")), niftiPath])
	nifti2glb.main("sample_lung.nii.gz", 0.5, fname + "_lungSegmented")
	success = subprocess.run(["rm", str(niftiPath.joinpath("sample_lung.nii.gz"))])
	print("lungDicom2glb: done")