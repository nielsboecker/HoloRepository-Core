import pytest
import os
import pathlib
from subprocess import check_output as checkOutput
import subprocess

newCwd = str(pathlib.Path(str(os.path.dirname(os.path.realpath(__file__)))).parent)

def test_main_s0_0():
	output = checkOutput('python pipelineController.py -c test/testList.json s0', cwd=newCwd, shell=True).decode("utf-8")
	assert "Hello World" in str(output)

def test_main_s0_1():
	output = ""
	try:
		output = subprocess.check_output('python pipelineController.py -c test/testList.json s0 -p 1', cwd=newCwd, shell=True).decode("utf-8")
	except subprocess.CalledProcessError as temp:
		output = temp.returncode
	assert "1" in str(output)

def test_main_s0_2():
	output = ""
	try:
		output = subprocess.check_output('python pipelineController.py -c test/testList.json s3', cwd=newCwd, shell=True).decode("utf-8")
	except subprocess.CalledProcessError as temp:
		output = temp.returncode
	assert "1" in str(output)
	'''output = checkOutput('python pipelineController.py -c test/testList.json s3', cwd=newCwd, shell=True).decode("utf-8")
	assert "pipelineController: no pipeline with such ID" in str(output)'''

def test_main_s0_3():
	output = ""
	try:
		output = subprocess.check_output('python pipelineController.py -c test/testList.json s3 -p 0', cwd=newCwd, shell=True).decode("utf-8")
	except subprocess.CalledProcessError as temp:
		output = temp.returncode
	assert "1" in str(output)
	'''output = checkOutput('python pipelineController.py -c test/testList.json s3 -p 0', cwd=newCwd, shell=True).decode("utf-8")
	assert "pipelineController: no pipeline with such ID" in str(output)'''

def test_main_ls():
	output = checkOutput('python pipelineController.py -c test/testList.json --ls', cwd=newCwd, shell=True).decode("utf-8")
	assert "dicom2glb" in str(output)

def test_main_info_0():
	output = checkOutput('python pipelineController.py -c test/testList.json --info dicom2glb', cwd=newCwd, shell=True).decode("utf-8")
	assert "description: Generate glb mesh from dicom" in str(output)

def test_main_info_1():
	output = checkOutput('python pipelineController.py -c test/testList.json --info doesNotExist', cwd=newCwd, shell=True).decode("utf-8")
	assert "pipelineController: no pipeline with such name" in str(output)
