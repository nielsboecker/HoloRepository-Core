import numpy as np
import nibabel as nib
import pathlib
'''from utils import *
from segment_lung import segment_lung
from segment_airway import segment_airway'''
niftiPath = pathlib.Path.cwd().joinpath("medicalScans", "nifti")


def main(fname):
	fname = str(fname).lower()#?
	import components.lungSegment.utils as utils
	from components.lungSegment.segment_lung import segment_lung
	from components.lungSegment.segment_airway import segment_airway

	params = utils.define_parameter()

#####################################################
# Load image 
#####################################################

	I         = nib.load(str(niftiPath.joinpath(str(fname))))
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



if __name__ == '__main__':
	import sys
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
