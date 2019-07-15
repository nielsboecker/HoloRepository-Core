from components import nifti2numpy
from components import numpy2obj
import pathlib
import sys
import numpy as np

niftiPath = pathlib.Path.cwd().joinpath("medicalScans", "nifti")

def main(niftiData, threshold, flipNpy):
	tempNpy = nifti2numpy.main(str(niftiPath.joinpath(niftiData)), niftiData)
	if flipNpy:
		tempNpy = np.flip(tempNpy, 0)
		tempNpy = np.flip(tempNpy, 1)
	numpy2obj.main(tempNpy, threshold, niftiData.replace(".nii.gz", "").replace(".nii", ""))
	print("nifti2obj: done")

if __name__ == "__main__":
	niftiData = sys.argv[1]
	threshold = sys.argv[2]
	flipNpy = sys.argv[3]
	main(niftiData, threshold, flipNpy)