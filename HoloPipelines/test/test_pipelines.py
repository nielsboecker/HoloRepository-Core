import os
import pytest
import pathlib
from subprocess import check_output as subpro

outputPath = pathlib.Path.cwd().joinpath("output")
objPath = outputPath.joinpath("OBJ")
glbPath = outputPath.joinpath("GLB")

newCwd = str(pathlib.Path(str(os.path.dirname(os.path.realpath(__file__)))).parent)

def test_pipelines_dicom2glb():
	output = subpro("python pipelineController.py p3 -p 3_Axial_CE 350", cwd=newCwd, shell=True).decode("utf-8")
	assert "dicom2numpy: resampling done" in str(output)
	assert "numpy2obj: done" in str(output)
	assert "dicom2glb: done" in str(output)
	assert os.path.isfile(glbPath.joinpath("3_Axial_CE.glb"))

def test_pipelines_lungDicom2glb():
	output = subpro("python pipelineController.py p4 -p 3_Axial_CE", cwd=newCwd, shell=True).decode("utf-8")
	assert "dcm2nifti: done" in str(output)
	assert "obj2gltf: conversion complete" in str(output)
	assert "lungDicom2glb: done" in str(output)
	assert os.path.isfile(glbPath.joinpath("3_Axial_CE_lungSegmented.glb"))

def test_pipelines_nifti2obj():
	output = subpro("python pipelineController.py p0 -p 1103_3_glm.nii 30 0", cwd=newCwd, shell=True).decode("utf-8")
	assert "nifti2obj: done" in str(output)
	assert os.path.isfile(objPath.joinpath("1103_3_glm.obj"))

def test_pipelines_nifti2glb():
	output = subpro("python pipelineController.py p1 -p 1103_3_glm.nii 30 0", cwd=newCwd, shell=True).decode("utf-8")
	assert "nifti2glb: done" in str(output)
	assert os.path.isfile(glbPath.joinpath("1103_3_glm.glb"))

