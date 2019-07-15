import os
import pytest
import pathlib
from subprocess import check_output as checkOutput
import subprocess

saveto = pathlib.Path.cwd()
dicomPath = saveto.joinpath("medicalScans", "dicom")
niftiPath = saveto.joinpath("medicalScans", "nifti")

outputPath = pathlib.Path.cwd().joinpath("output")
objPath = outputPath.joinpath("OBJ")
glbPath = outputPath.joinpath("GLB")

newCwd = str(pathlib.Path(str(os.path.dirname(os.path.realpath(__file__)))).parent)

@pytest.fixture
def testSetup():
	print('Beginning dicom sample download...')

	if not os.path.exists(str(niftiPath.joinpath("1103_3_glm.nii"))) and os.path.exists(str(dicomPath.joinpath("3_Axial_CE"))):

		url = 'https://holoblob.blob.core.windows.net/test/3_Axial_CE.zip'
		urllib.request.urlretrieve(url, str(saveto.joinpath("__temp__.zip"))) 

		print('Beginning dicom unzip...')
		with ZipFile('__temp__.zip', 'r') as zipObj:
			zipObj.extractall(str(dicomPath))
		os.remove('__temp__.zip')

		#download nifti
		print('Beginning nifti sample download...')

		url = 'https://holoblob.blob.core.windows.net/test/1103_3_glm.nii.zip'  
		urllib.request.urlretrieve(url, str(saveto.joinpath("__temp__.zip"))) 

		print('Beginning nifti unzip...')
		with ZipFile('__temp__.zip', 'r') as zipObj:
			zipObj.extractall(str(niftiPath))
		os.remove('__temp__.zip')

		print("setup: done")

	if os.path.exists(str(glbPath.joinpath("3_Axial_CE.glb"))):#have them for each test case?
		os.remove(str(glbPath.joinpath("3_Axial_CE.glb")))

	if os.path.exists(str(glbPath.joinpath("3_Axial_CE_lungSegmented.glb"))):
		os.remove(str(glbPath.joinpath("3_Axial_CE_lungSegmented.glb")))

	if os.path.exists(str(objPath.joinpath("1103_3_glm.obj"))):
		os.remove(str(objPath.joinpath("1103_3_glm.obj")))

	if os.path.exists(str(glbPath.joinpath("1103_3_glm.glb"))):
		os.remove(str(glbPath.joinpath("1103_3_glm.glb")))

	setupEndsHere = True

	yield setupEndsHere

	if os.path.exists(str(glbPath.joinpath("3_Axial_CE.glb"))):#have them for each test case?
		os.remove(str(glbPath.joinpath("3_Axial_CE.glb")))

	if os.path.exists(str(glbPath.joinpath("3_Axial_CE_lungSegmented.glb"))):
		os.remove(str(glbPath.joinpath("3_Axial_CE_lungSegmented.glb")))

	if os.path.exists(str(objPath.joinpath("1103_3_glm.obj"))):
		os.remove(str(objPath.joinpath("1103_3_glm.obj")))

	if os.path.exists(str(glbPath.joinpath("1103_3_glm.glb"))):
		os.remove(str(glbPath.joinpath("1103_3_glm.glb")))

def test_pipelines_dicom2glb(testSetup):
	output = checkOutput("python pipelineController.py -c test/testList.json p3 -p 3_Axial_CE 350", cwd=newCwd, shell=True).decode("utf-8")
	assert "dicom2numpy: resampling done" in str(output)
	assert "numpy2obj: done" in str(output)
	assert "dicom2glb: done" in str(output)
	assert os.path.isfile(glbPath.joinpath("3_Axial_CE.glb"))

def test_pipelines_lungDicom2glb(testSetup):
	output = checkOutput("python pipelineController.py -c test/testList.json p4 -p 3_Axial_CE", cwd=newCwd, shell=True).decode("utf-8")
	assert "dcm2nifti: done" in str(output)
	assert "obj2gltf: conversion complete" in str(output)
	assert "lungDicom2glb: done" in str(output)
	assert os.path.isfile(glbPath.joinpath("3_Axial_CE_lungSegmented.glb"))

def test_pipelines_nifti2obj(testSetup):
	output = checkOutput("python pipelineController.py -c test/testList.json p0 -p 1103_3_glm.nii 30 0", cwd=newCwd, shell=True).decode("utf-8")
	assert "nifti2obj: done" in str(output)
	assert os.path.isfile(objPath.joinpath("1103_3_glm.obj"))

def test_pipelines_nifti2glb(testSetup):
	output = checkOutput("python pipelineController.py -c test/testList.json p1 -p 1103_3_glm.nii 30 0", cwd=newCwd, shell=True).decode("utf-8")
	assert "nifti2glb: done" in str(output)
	assert os.path.isfile(glbPath.joinpath("1103_3_glm.glb"))

