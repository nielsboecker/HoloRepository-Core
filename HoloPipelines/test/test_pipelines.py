import os
import pytest
import pathlib
import subprocess

import urllib.request
from zipfile import ZipFile

thisCwd = pathlib.Path.cwd()
dicomPath = thisCwd.joinpath("medicalScans", "dicom")
niftiPath = thisCwd.joinpath("medicalScans", "nifti")

outputPath = pathlib.Path.cwd().joinpath("output")
objPath = outputPath.joinpath("OBJ")
glbPath = outputPath.joinpath("GLB")

newCwd = str(pathlib.Path(str(os.path.dirname(os.path.realpath(__file__)))).parent)


@pytest.fixture
def testSetup():
    print("Beginning dicom sample download...")

    if not os.path.exists(str(dicomPath.joinpath("3_Axial_CE"))):
        # download dicom sample
        print("Beginning dicom sample download...")

        url = "https://holoblob.blob.core.windows.net/test/3_Axial_CE.zip"
        urllib.request.urlretrieve(url, str(thisCwd.joinpath("__temp__.zip")))

        print("Beginning dicom unzip...")
        with ZipFile("__temp__.zip", "r") as zipObj:  # unzip
            zipObj.extractall(str(dicomPath))
        os.remove("__temp__.zip")

    if not os.path.exists(str(niftiPath.joinpath("1103_3_glm.nii"))):
        # download nifti sample
        print("Beginning nifti sample download...")

        url = "https://holoblob.blob.core.windows.net/test/1103_3_glm.nii.zip"
        urllib.request.urlretrieve(url, str(thisCwd.joinpath("__temp__.zip")))

        print("Beginning nifti unzip...")
        with ZipFile("__temp__.zip", "r") as zipObj:  # unzip
            zipObj.extractall(str(niftiPath))
        os.remove("__temp__.zip")

        print("setup: done")

    remove3Dmodels()

    yield  # code below will run everytime a test case finishes

    remove3Dmodels()


def remove3Dmodels():
    if os.path.exists(str(glbPath.joinpath("testResult0.glb"))):
        os.remove(str(glbPath.joinpath("testResult0.glb")))

    if os.path.exists(str(glbPath.joinpath("testResult1.glb"))):
        os.remove(str(glbPath.joinpath("testResult1.glb")))

    if os.path.exists(str(objPath.joinpath("testResult2.obj"))):
        os.remove(str(objPath.joinpath("testResult2.obj")))

    if os.path.exists(str(glbPath.joinpath("testResult3.glb"))):
        os.remove(str(glbPath.joinpath("testResult3.glb")))


def test_pipelines_dicom2glb(testSetup):
    output = subprocess.run(
        [
            "python",
            "pipelineController.py",
            "-c",
            "test/testList.json",
            "p3",
            "-p",
            str(dicomPath.joinpath("3_Axial_CE")),
            str(glbPath.joinpath("testResult0.glb")),
            "350",
        ],
        cwd=newCwd,
    )
    assert 0 == output.returncode
    assert os.path.isfile(glbPath.joinpath("testResult0.glb"))


def test_pipelines_lungDicom2glb(testSetup):
    output = subprocess.run(
        [
            "python",
            "pipelineController.py",
            "-c",
            "test/testList.json",
            "p4",
            "-p",
            str(dicomPath.joinpath("3_Axial_CE")),
            str(glbPath.joinpath("testResult1.glb")),
        ],
        cwd=newCwd,
    )
    assert 0 == output.returncode
    assert os.path.isfile(glbPath.joinpath("testResult1.glb"))


def test_pipelines_nifti2obj(testSetup):
    output = subprocess.run(
        [
            "python",
            "pipelineController.py",
            "-c",
            "test/testList.json",
            "p0",
            "-p",
            str(niftiPath.joinpath("1103_3_glm.nii")),
            str(objPath.joinpath("testResult2.obj")),
            "30",
            "0",
        ],
        cwd=newCwd,
    )
    assert 0 == output.returncode
    assert os.path.isfile(objPath.joinpath("testResult2.obj"))


def test_pipelines_nifti2glb(testSetup):
    output = subprocess.run(
        [
            "python",
            "pipelineController.py",
            "-c",
            "test/testList.json",
            "p1",
            "-p",
            str(niftiPath.joinpath("1103_3_glm.nii")),
            str(glbPath.joinpath("testResult3.glb")),
            "30",
        ],
        cwd=newCwd,
    )
    assert 0 == output.returncode
    assert os.path.isfile(glbPath.joinpath("testResult3.glb"))
