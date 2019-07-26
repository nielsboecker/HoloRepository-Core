import os
import shutil

if not os.path.exists("medicalScans"):
    os.mkdir("medicalScans")
    os.mkdir("medicalScans/dicom")
    os.mkdir("medicalScans/nifti")
else:
    shutil.rmtree("medicalScans")
    os.mkdir("medicalScans")
    os.mkdir("medicalScans/dicom")
    os.mkdir("medicalScans/nifti")

if not os.path.exists("numpy"):
    os.mkdir("numpy")
else:
    shutil.rmtree("numpy")
    os.mkdir("numpy")

if not os.path.exists("output"):
    os.mkdir("output")
    os.mkdir("output/OBJ")
    os.mkdir("output/GLB")
else:
    shutil.rmtree("output")
    os.mkdir("output")
    os.mkdir("output/OBJ")
    os.mkdir("output/GLB")

print("clean up: done")
