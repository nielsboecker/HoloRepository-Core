import dicom2nifti
import os
import glob
import pathlib


def main(dicomInputPath, outputNiftiFolderPath):
    # check if sub dirs exist
    if not os.path.exists(outputNiftiFolderPath):
        os.makedirs(outputNiftiFolderPath)
    # convert series of dicom to nifti
    dicom2nifti.convert_directory(dicomInputPath, outputNiftiFolderPath)
    print("dcm2nifti: done")
    lsdir = glob.glob(str(pathlib.Path(outputNiftiFolderPath).joinpath("*.nii.gz")))
    outputNiftiPath = str(pathlib.Path(lsdir[0]))
    return outputNiftiPath


if __name__ == "__main__":
    print("component can't run on its own")
