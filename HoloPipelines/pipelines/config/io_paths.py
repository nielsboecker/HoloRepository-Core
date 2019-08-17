import pathlib
import os

# TODO: nifty variable is used in other components, even though the dir is not /job/<id>/...
# TODO: Should be refactored, but not sure if still up to date with the /job/id concept
cwd = pathlib.Path.cwd()
medical_scans_path = cwd.joinpath("medicalScans")
dicom_path = cwd.joinpath("medicalScans", "dicom")
nifti_path = cwd.joinpath("medicalScans", "nifti")
output_path = cwd.joinpath("output")
obj_path = cwd.joinpath("output", "obj")
glb_path = cwd.joinpath("output", "glb")


# TODO: This is not just a list of paths, it also creates dirs, so it's not just config
# TODO: is this still in line with the /jobs/<id>/... concept?
def create_common_dirs():
    for path in [medical_scans_path, dicom_path, nifti_path, output_path, obj_path, glb_path]:
        if not os.path.exists(str(path)):
            os.mkdir(str(path))
