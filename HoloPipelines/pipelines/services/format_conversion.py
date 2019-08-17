from components import compDicom2numpy
import nibabel as nib
import numpy as np


def convert_dicom_to_nifty(dicomInputPath, niftiOutputPath):
    # convert series of dicom to numpy
    dicomNumpyList = compDicom2numpy.main(dicomInputPath)

    # convert numpy array to nifti image
    niftiImage = nib.Nifti1Image(dicomNumpyList, affine=np.eye(4))
    nib.save(niftiImage, niftiOutputPath)

    return niftiOutputPath
