import os
import pytest
import pathlib
import subprocess
import logging
import shutil
import threading

import urllib.request
import requests
from zipfile import ZipFile
from http.server import BaseHTTPRequestHandler, HTTPServer

thisCwd = pathlib.Path.cwd()
zipFileName = "__temp__.zip"
segmentedAbdomenFileName = "__segmentedAbdomen__.nii.gz"
dicomPath = thisCwd.joinpath("medicalScans", "dicom")
niftiPath = thisCwd.joinpath("medicalScans", "nifti")

outputPath = pathlib.Path.cwd().joinpath("output")
objPath = outputPath.joinpath("obj")
glbPath = outputPath.joinpath("glb")

newCwd = str(pathlib.Path(str(os.path.dirname(os.path.realpath(__file__)))).parent)


class testServer(BaseHTTPRequestHandler):
    def do_POST(self):
        length = self.headers["content-length"]
        data = self.rfile.read(int(length))

        if not data:
            logging.warning("error in testServer")

        self.send_response(200)
        self.end_headers()

        with open(str(niftiPath.joinpath(segmentedAbdomenFileName)), "rb") as toSend:
            self.wfile.write(toSend.read())  # Read the file and send the contents


@pytest.fixture
def testSetup():
    logging.info("Checking for sample files...")

    if not os.path.exists(str(dicomPath.joinpath("3_Axial_CE"))):
        # download dicom sample
        logging.info("Beginning dicom (1/2) sample download...")

        url = "https://holoblob.blob.core.windows.net/test/3_Axial_CE.zip"
        urllib.request.urlretrieve(url, str(thisCwd.joinpath(zipFileName)))

        logging.info("Beginning dicom unzip...")
        with ZipFile(zipFileName, "r") as zipObj:  # unzip
            zipObj.extractall(str(dicomPath))
        os.remove(zipFileName)

    if not os.path.exists(str(dicomPath.joinpath("abdomen"))):
        # download dicom sample
        logging.info("Beginning dicom (2/2) sample download...")

        url = "https://dl.dropbox.com/s/tuxko4lycrz790b/abdomen.zip?dl=1"
        urllib.request.urlretrieve(url, str(thisCwd.joinpath(zipFileName)))

        logging.info("Beginning dicom unzip...")
        with ZipFile(zipFileName, "r") as zipObj:  # unzip
            zipObj.extractall(str(dicomPath))
        os.remove(zipFileName)

    if not os.path.exists(str(niftiPath.joinpath("1103_3_glm.nii"))):
        # download nifti sample
        logging.info("Beginning nifti sample download...")

        url = "https://holoblob.blob.core.windows.net/test/1103_3_glm.nii.zip"
        urllib.request.urlretrieve(url, str(thisCwd.joinpath(zipFileName)))

        logging.info("Beginning nifti unzip...")
        with ZipFile(zipFileName, "r") as zipObj:  # unzip
            zipObj.extractall(str(niftiPath))
        os.remove(zipFileName)

    logging.info("setup: done")

    remove3Dmodels()

    yield  # code below will run everytime a test case finishes

    remove3Dmodels()


@pytest.fixture
def setupMockPOSTresponse():
    logging.info("Downloading mock output...")
    urlNiftyOut = (
        "https://dl.dropbox.com/s/x6b5cc34h4alya6/Owenpap___niftynet_out.nii.gz?dl=1"
    )
    response = requests.get(urlNiftyOut)
    open(str(niftiPath.joinpath(segmentedAbdomenFileName)), "wb+").write(
        response.content
    )

    logging.info("Starting NN model mock server...")
    myServer = HTTPServer(("localhost", 4567), testServer)
    threading.Thread(target=myServer.serve_forever, daemon=True).start()

    yield

    # remove nii file
    if os.path.exists(str(niftiPath.joinpath(segmentedAbdomenFileName))):
        os.remove(str(niftiPath.joinpath(segmentedAbdomenFileName)))

    if os.path.exists(str(niftiPath.joinpath("dataFromPost.nii"))):
        os.remove(str(niftiPath.joinpath("dataFromPost.nii")))

    # remove abdomen CT Dicom files
    if os.path.exists(str(dicomPath.joinpath("abdomen"))):
        shutil.rmtree(str(dicomPath.joinpath("abdomen")))


def remove3Dmodels():
    if os.path.exists(str(glbPath.joinpath("testResult0.glb"))):
        os.remove(str(glbPath.joinpath("testResult0.glb")))

    if os.path.exists(str(glbPath.joinpath("testResult1.glb"))):
        os.remove(str(glbPath.joinpath("testResult1.glb")))

    if os.path.exists(str(objPath.joinpath("testResult2.obj"))):
        os.remove(str(objPath.joinpath("testResult2.obj")))

    if os.path.exists(str(glbPath.joinpath("testResult3.glb"))):
        os.remove(str(glbPath.joinpath("testResult3.glb")))

    if os.path.exists(str(glbPath.joinpath("testResult4.glb"))):
        os.remove(str(glbPath.joinpath("testResult4.glb")))

    if os.path.exists(str(glbPath.joinpath("organNo1.glb"))):
        os.remove(str(glbPath.joinpath("organNo1.glb")))

    if os.path.exists(str(glbPath.joinpath("organNo2.glb"))):
        os.remove(str(glbPath.joinpath("organNo2.glb")))

    if os.path.exists(str(glbPath.joinpath("organNo3.glb"))):
        os.remove(str(glbPath.joinpath("organNo3.glb")))

    if os.path.exists(str(glbPath.joinpath("organNo4.glb"))):
        os.remove(str(glbPath.joinpath("organNo4.glb")))

    if os.path.exists(str(glbPath.joinpath("organNo5.glb"))):
        os.remove(str(glbPath.joinpath("organNo5.glb")))

    if os.path.exists(str(glbPath.joinpath("organNo6.glb"))):
        os.remove(str(glbPath.joinpath("organNo6.glb")))

    if os.path.exists(str(glbPath.joinpath("organNo7.glb"))):
        os.remove(str(glbPath.joinpath("organNo7.glb")))

    if os.path.exists(str(glbPath.joinpath("organNo8.glb"))):
        os.remove(str(glbPath.joinpath("organNo8.glb")))


def test_pipelines_dicom2glb(testSetup):
    output = subprocess.run(
        [
            "python",
            "pipelineController.py",
            "-c",
            "test/pipelineListForTesting.json",
            "dicom2glb",
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
            "test/pipelineListForTesting.json",
            "lungDicom2glb",
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
            "test/pipelineListForTesting.json",
            "nifti2obj",
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
            "test/pipelineListForTesting.json",
            "nifti2glb",
            "-p",
            str(niftiPath.joinpath("1103_3_glm.nii")),
            str(glbPath.joinpath("testResult3.glb")),
            "30",
        ],
        cwd=newCwd,
    )
    assert 0 == output.returncode
    assert os.path.isfile(glbPath.joinpath("testResult3.glb"))


def test_pipelines_abdomenDicom2glb(setupMockPOSTresponse, testSetup):
    output = subprocess.run(
        [
            "python",
            "pipelineController.py",
            "-c",
            "test/pipelineListForTesting.json",
            "abdomenDicom2glb",
            "-p",
            str(dicomPath.joinpath("abdomen")),
            str(glbPath),
            "http://localhost:4567",
        ],
        cwd=newCwd,
    )
    assert 0 == output.returncode
    assert os.path.isfile(glbPath.joinpath("organNo1.glb"))
    assert os.path.isfile(glbPath.joinpath("organNo2.glb"))
    assert os.path.isfile(glbPath.joinpath("organNo3.glb"))
    assert os.path.isfile(glbPath.joinpath("organNo4.glb"))
    assert os.path.isfile(glbPath.joinpath("organNo5.glb"))
    assert os.path.isfile(glbPath.joinpath("organNo6.glb"))
    assert os.path.isfile(glbPath.joinpath("organNo7.glb"))
    assert os.path.isfile(glbPath.joinpath("organNo8.glb"))
