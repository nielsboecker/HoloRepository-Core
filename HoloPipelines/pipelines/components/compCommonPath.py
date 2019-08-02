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
    for path in [medicalScans, dicom, nifti, output, obj, glb]:
    	if not os.path.exists(str(path)):
        	os.mkdir(str(path))


if __name__ == "__main__":
    main()
