import pytest
from pipelineController import main
import os
import pipelines.components.fileHandler as fileHand

def test_main_s0_0():
	output = os.popen('python pipelineController.py s0').read()
	assert "Hello World" in str(output)

def test_main_s0_1():
	output = os.popen('python pipelineController.py s0 -p 1').read()
	assert "pipelineController: invalid number of param" in str(output)

def test_main_s0_2():
	output = os.popen('python pipelineController.py s3').read()
	assert "pipelineController: no pipeline with such ID" in str(output)

def test_main_s0_2():
	output = os.popen('python pipelineController.py s3 -p 0').read()
	assert "pipelineController: no pipeline with such ID" in str(output)

'''def test_main_p1():
	output = os.popen('python pipelineController.py p1 -p 1103_3_glm.nii 30 0').read()
	assert "nifti2glb: done" in str(output)
	assert os.path.isfile(fileHand.glbPath + "1103_3_glm.glb")'''#moved to test_pipelines

def test_main_ls():
	output = os.popen('python pipelineController.py --ls').read()
	assert "dicom2glb" in str(output)

def test_main_info_0():
	output = os.popen('python pipelineController.py --info dicom2glb').read()
	assert "description: Generate glb mesh from dicom" in str(output)

def test_main_info_1():
	output = os.popen('python pipelineController.py --info doesNotExist').read()
	assert "pipelineController: no pipeline with such name" in str(output)
