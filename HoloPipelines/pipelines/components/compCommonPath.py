import pathlib
import os

cwd = pathlib.Path.cwd()
medicalScans = cwd.joinpath("medicalScans")
dicom = cwd.joinpath("medicalScans", "dicom")
nifti = cwd.joinpath("medicalScans", "nifti")
output = cwd.joinpath("output")
obj = cwd.joinpath("output", "obj")
glb = cwd.joinpath("output", "glb")


def main():
    if not os.path.exists(str(medicalScans)):
        os.mkdir(str(medicalScans))
        os.mkdir(str(dicom))
        os.mkdir(str(nifti))
    if not os.path.exists(str(output)):
        os.mkdir(str(output))
        os.mkdir(str(obj))
        os.mkdir(str(glb))


if __name__ == "__main__":
    main()
