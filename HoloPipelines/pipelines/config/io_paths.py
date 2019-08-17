import pathlib
import os


cwd = pathlib.Path.cwd()
medicalScans = cwd.joinpath("medicalScans")
dicom = cwd.joinpath("medicalScans", "dicom")
nifti = cwd.joinpath("medicalScans", "nifti")
output = cwd.joinpath("output")
obj = cwd.joinpath("output", "obj")
glb = cwd.joinpath("output", "glb")


# TODO: This is not just a list of paths, it also creates dirs, so it's not just config
# TODO: is this still in line with the /jobs/<id>/... concept?
def create_common_dirs():
    for path in [medicalScans, dicom, nifti, output, obj, glb]:
        if not os.path.exists(str(path)):
            os.mkdir(str(path))
