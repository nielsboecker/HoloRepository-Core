import dicom2nifti
import pathlib
import os


def main(dicomInputPath, outputNiftiFolderPath):
    # check if sub dirs exist
    if not os.path.exists(outputNiftiFolderPath):
        os.makedirs(outputNiftiFolderPath)
    # convert series of dicom to nifti
    dicom2nifti.convert_directory(dicomInputPath, outputNiftiFolderPath)
    print("dcm2nifti: done")
    return outputNiftiFolderPath


if __name__ == "__main__":
    print("component can't run on its own")
