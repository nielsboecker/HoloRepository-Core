import pytest
import os
import pathlib
import subprocess

newCwd = str(pathlib.Path(str(os.path.dirname(os.path.realpath(__file__)))).parent)

def test_main_s0_normal():
	output = subprocess.run(["python", "pipelineController.py", "-c", "test/testList.json", "s0"], cwd=newCwd)
	assert 0 == output.returncode

def test_main_s0_invalid_number_of_argument():
	output = subprocess.run(["python", "pipelineController.py", "-c", "test/testList.json", "s0", "-p", "1"], cwd=newCwd)
	assert 1 == output.returncode

def test_main_missing_pipeline():
	output = subprocess.run(["python", "pipelineController.py", "-c", "test/testList.json", "s3"], cwd=newCwd)
	assert 1 == output.returncode

def test_main_s0_missing_pipeline_with_extra_arguments():
	output = subprocess.run(["python", "pipelineController.py", "-c", "test/testList.json", "s3", "-p", "0"], cwd=newCwd)
	assert 1 == output.returncode

def test_main_ls_normal():
	output = subprocess.run(["python", "pipelineController.py", "-c", "test/testList.json", "--ls"], cwd=newCwd)
	assert 0 == output.returncode

def test_main_info_dicom2glb():
	output = subprocess.run(["python", "pipelineController.py", "-c", "test/testList.json", "--info", "dicom2glb"], cwd=newCwd)
	assert 0 == output.returncode

def test_main_info_for_missing_pipeline():
	output = subprocess.run(["python", "pipelineController.py", "-c", "test/testList.json", "--info", "doesNotExist"], cwd=newCwd)
	assert 1 == output.returncode
