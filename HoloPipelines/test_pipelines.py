import os
#os.chdir("..")
import pytest
#from pipelineController import main
import pathlib

outputPath = pathlib.Path.cwd().joinpath("output")
objPath = outputPath.joinpath("OBJ")
glbPath = outputPath.joinpath("GLB")

def test_pipelines_dicom2glb():
	output = os.popen("python pipelineController.py p3 -p 3_Axial_CE 350").read()
	#output = os.popen("python pipelines/dicom2glb.py 3_Axial_CE 350").read()
	assert "dicom2numpy: resampling done" in str(output)
	assert "numpy2obj: done" in str(output)
	assert "dicom2glb: done" in str(output)
	assert os.path.isfile(glbPath.joinpath("3_Axial_CE.glb"))

def test_pipelines_lungDicom2glb():
	output = os.popen("python pipelineController.py p4 -p 3_Axial_CE").read()
	assert "dcm2nifti: done" in str(output)
	assert "obj2gltf: conversion complete" in str(output)
	assert "lungDicom2glb: done" in str(output)
	assert os.path.isfile(glbPath.joinpath("3_Axial_CE_lungSegmented.glb"))

def test_pipelines_nifti2obj():
	output = os.popen("python pipelineController.py p0 -p 1103_3_glm.nii 30 0").read()
	assert "nifti2obj: done" in str(output)
	assert os.path.isfile(objPath.joinpath("1103_3_glm.obj"))

def test_pipelines_nifti2glb():
	output = os.popen("python pipelineController.py p1 -p 1103_3_glm.nii 30 0").read()
	assert "nifti2glb: done" in str(output)
	assert os.path.isfile(glbPath.joinpath("1103_3_glm.glb"))

