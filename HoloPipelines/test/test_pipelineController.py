import pytest
import os
import pathlib
from subprocess import check_output as subpro

newCwd = str(pathlib.Path(str(os.path.dirname(os.path.realpath(__file__)))).parent)

def test_main_s0_0():
	output = subpro('python pipelineController.py s0', cwd=newCwd, shell=True).decode("utf-8")
	assert "Hello World" in str(output)

def test_main_s0_1():
	output = subpro('python pipelineController.py s0 -p 1', cwd=newCwd, shell=True).decode("utf-8")
	assert "pipelineController: invalid number of param" in str(output)

def test_main_s0_2():
	output = subpro('python pipelineController.py s3', cwd=newCwd, shell=True).decode("utf-8")
	assert "pipelineController: no pipeline with such ID" in str(output)

def test_main_s0_2():
	output = subpro('python pipelineController.py s3 -p 0', cwd=newCwd, shell=True).decode("utf-8")
	assert "pipelineController: no pipeline with such ID" in str(output)

def test_main_ls():
	output = subpro('python pipelineController.py --ls', cwd=newCwd, shell=True).decode("utf-8")
	assert "dicom2glb" in str(output)

def test_main_info_0():
	output = subpro('python pipelineController.py --info dicom2glb', cwd=newCwd, shell=True).decode("utf-8")
	assert "description: Generate glb mesh from dicom" in str(output)

def test_main_info_1():
	output = subpro('python pipelineController.py --info doesNotExist', cwd=newCwd, shell=True).decode("utf-8")
	assert "pipelineController: no pipeline with such name" in str(output)
