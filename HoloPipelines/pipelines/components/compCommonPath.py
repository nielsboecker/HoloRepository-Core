import pathlib

cwd = pathlib.Path.cwd()
dicom = cwd.joinpath("medicalScans", "dicom")
nifti = cwd.joinpath("medicalScans", "nifti")
obj = cwd.joinpath("output", "obj")
glb = cwd.joinpath("output", "glb")