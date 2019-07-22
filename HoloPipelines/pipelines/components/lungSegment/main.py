import numpy as np
import nibabel as nib
import pathlib
import os
import glob
import sys

niftiPath = pathlib.Path.cwd().joinpath("medicalScans", "nifti")

if not os.path.exists("pipelines/components/lungSegment/result"):
		os.mkdir("pipelines/components/lungSegment")
		os.mkdir("pipelines/components/lungSegment/result")


def main(inputNiftiPath):
	inputNiftiPath = str(inputNiftiPath)
	import components.lungSegment.utils as utils
	from components.lungSegment.segment_lung import segment_lung
	from components.lungSegment.segment_airway import segment_airway

	params = utils.define_parameter()

	if not ".nii" in inputNiftiPath:
		lsdir = glob.glob(str(pathlib.Path(inputNiftiPath).joinpath("*.nii.gz")))
		if len(lsdir) != 1:
			sys.exit("lungSegment.main: error, invalid number of Nifti file found inside folder " + inputNiftiPath)
		inputNiftiPath = str(pathlib.Path(lsdir[0]))

#####################################################
# Load image 
#####################################################

	I         = nib.load(inputNiftiPath)
	I_affine  = I.affine
	I         = I.get_data()

#####################################################
# Coarse segmentation of lung & airway 
#####################################################

	Mlung = segment_lung(params, I, I_affine)

#####################################################
# Romove airway from lung mask 
#####################################################

	Mlung, Maw = segment_airway(params, I, I_affine, Mlung)

	return str(pathlib.Path.cwd().joinpath("pipelines", "components", "lungSegment", "result", "sample_lung.nii.gz"))



if __name__ == '__main__':
	try:
		from utils import *
		from segment_lung import segment_lung
		from segment_airway import segment_airway

		params = define_parameter()
	except:
		import components.lungSegment.utils as untils
		from components.lungSegment.segment_lung import segment_lung
		from components.lungSegment.segment_airway import segment_airway

		params = untils.define_parameter()

#####################################################
# Load image 
#####################################################

	I         = nib.load(niftiPath + sys.argv[1])
	I_affine  = I.affine
	I         = I.get_data()

#####################################################
# Coarse segmentation of lung & airway 
#####################################################

	Mlung = segment_lung(params, I, I_affine)

#####################################################
# Romove airway from lung mask 
#####################################################

	Mlung, Maw = segment_airway(params, I, I_affine, Mlung)
