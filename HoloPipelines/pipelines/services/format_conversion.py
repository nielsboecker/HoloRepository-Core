import logging

from components import compDicom2numpy
import nibabel as nib
import numpy as np

from pipelines.services.marching_cubes import generate_obj


def convert_dicom_to_nifty(dicomInputPath, niftiOutputPath):
    # convert series of dicom to numpy
    dicomNumpyList = compDicom2numpy.main(dicomInputPath)

    # convert numpy array to nifti image
    niftiImage = nib.Nifti1Image(dicomNumpyList, affine=np.eye(4))
    nib.save(niftiImage, niftiOutputPath)

    return niftiOutputPath


def convert_numpy_to_obj(input_data, main_threshold, output_path):
    generate_obj(input_data, main_threshold, output_path)
    logging.info("numpy2obj: done")
    return output_path