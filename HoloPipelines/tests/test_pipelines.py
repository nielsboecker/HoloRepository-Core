import logging
import os
import pathlib
import shutil
import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from zipfile import ZipFile

import pytest
import requests


pythonPath = sys.executable
thisCwd = pathlib.Path.cwd()
zipFileName = "__temp__.zip"
segmentedAbdomenFileName = "__segmentedAbdomen__.nii.gz"
dicomPath = thisCwd.joinpath("__test_input__", "dicom")
niftiPath = thisCwd.joinpath("__test_input__", "nifti")

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
    sampleFileDict = {
        str(dicomPath.joinpath("3_Axial_CE")): [
            "https://holoblob.blob.core.windows.net/test/3_Axial_CE.zip",
            str(dicomPath),
        ],
        str(dicomPath.joinpath("abdomen")): [
            "https://holoblob.blob.core.windows.net/mock-pacs/abdomen.zip",
            str(dicomPath),
        ],
        str(niftiPath.joinpath("1103_3_glm.nii")): [
            "https://holoblob.blob.core.windows.net/test/1103_3_glm.nii.zip",
            str(niftiPath),
        ],
    }

    for filePath, fileData in sampleFileDict.items():
        if not os.path.exists(filePath):
            # download dicom sample
            logging.info("Downloading sample file [{}]...".format(fileData[0]))

            url = fileData[0]
            saveTo = fileData[1]

            response = requests.get(url)
            open(str(thisCwd.joinpath(zipFileName)), "wb+").write(response.content)

            logging.info("Decompressing...")
            with ZipFile(zipFileName, "r") as zipObj:  # unzip
                zipObj.extractall(saveTo)
            os.remove(zipFileName)

    # download data for mock server (not in loop above as this one does not come in zip)
    if not os.path.exists(str(niftiPath.joinpath(segmentedAbdomenFileName))):
        urlNiftyOut = "https://holoblob.blob.core.windows.net/mock-pacs/Owenpap___niftynet_out.nii.gz"
        response = requests.get(urlNiftyOut)
        open(str(niftiPath.joinpath(segmentedAbdomenFileName)), "wb+").write(
            response.content
        )

    logging.info("setup: done")

    remove3Dmodels()

    yield  # code below will run everytime a tests case finishes

    remove3Dmodels()


@pytest.fixture
def setupMockPOSTresponse():
    logging.info("Starting NN model mock server...")
    myServer = HTTPServer(("localhost", 4567), testServer)
    threading.Thread(target=myServer.serve_forever, daemon=True).start()

    yield

    # remove files
    downloadedSampleFileList = [
        str(niftiPath.joinpath(segmentedAbdomenFileName)),
        str(niftiPath.joinpath("dataFromPost.nii")),
    ]

    for fileToDelete in downloadedSampleFileList:
        if os.path.exists(fileToDelete):
            os.remove(fileToDelete)

    if os.path.exists(str(dicomPath.joinpath("abdomen"))):
        shutil.rmtree(str(dicomPath.joinpath("abdomen")))


def remove3Dmodels():
    generatedMeshList = [
        str(glbPath.joinpath("testResult0.glb")),
        str(glbPath.joinpath("testResult1.glb")),
        str(objPath.joinpath("testResult2.obj")),
        str(glbPath.joinpath("testResult3.glb")),
        str(glbPath.joinpath("testResult4.glb")),
        str(glbPath.joinpath("organNo1.glb")),
        str(glbPath.joinpath("organNo2.glb")),
        str(glbPath.joinpath("organNo3.glb")),
        str(glbPath.joinpath("organNo4.glb")),
        str(glbPath.joinpath("organNo5.glb")),
        str(glbPath.joinpath("organNo6.glb")),
        str(glbPath.joinpath("organNo7.glb")),
        str(glbPath.joinpath("organNo8.glb")),
    ]

    for meshFileName in generatedMeshList:
        if os.path.exists(meshFileName):
            os.remove(meshFileName)


# FIXME: Fix this tests. It is completely outdated, as the commponent now downloads and posts stuff
#
# def test_pipelines_dicom2glb(testSetup):
#     output = subprocess.run(
#         [
#             pythonPath,
#             "pipeline_runner.py",
#             "-c",
#             "./core/pipelines/pipelines.json",
#             "dicom2glb",
#             "-p",
#             str(dicomPath.joinpath("3_Axial_CE")),
#             str(glbPath.joinpath("testResult0.glb")),
#             "350",
#         ],
#         cwd=newCwd,
#     )
#
#     assert 0 == output.returncode
#
#     assert os.path.isfile(glbPath.joinpath("testResult0.glb"))


# FIXME: Fix this tests. It is completely outdated, as the commponent now downloads and posts stuff
#
# def test_pipelines_lungDicom2glb(testSetup):
#     output = subprocess.run(
#         [
#             pythonPath,
#             "pipeline_runner.py",
#             "-c",
#             "./core/pipelines/pipelines.json",
#             "lungDicom2glb",
#             "-p",
#             str(dicomPath.joinpath("3_Axial_CE")),
#             str(glbPath.joinpath("testResult1.glb")),
#         ],
#         cwd=newCwd,
#     )
#
#     assert 0 == output.returncode
#     assert os.path.isfile(glbPath.joinpath("testResult1.glb"))


# FIXME: How is this supposed to work on the build server Pap?? The segmentation model is not running if you don't
# start it. And why did you change the port to that wild number??
#
# def test_pipelines_abdomenDicom2glb(setupMockPOSTresponse, testSetup):
#     output = subprocess.run(
#         [
#             pythonPath,
#             "pipeline_runner.py",
#             "-c",
#             "./core/pipelines/pipelines.json",
#             "abdomenDicom2glb",
#             "-p",
#             str(dicomPath.joinpath("abdomen")),
#             str(glbPath),
#             "http://localhost:4567",
#             "300",
#         ],
#         cwd=newCwd,
#     )
#     assert 0 == output.returncode
#     assert os.path.isfile(glbPath.joinpath("organNo1.glb"))
#     assert os.path.isfile(glbPath.joinpath("organNo2.glb"))
#     assert os.path.isfile(glbPath.joinpath("organNo3.glb"))
#     assert os.path.isfile(glbPath.joinpath("organNo4.glb"))
#     assert os.path.isfile(glbPath.joinpath("organNo5.glb"))
#     assert os.path.isfile(glbPath.joinpath("organNo6.glb"))
#     assert os.path.isfile(glbPath.joinpath("organNo7.glb"))
#     assert os.path.isfile(glbPath.joinpath("organNo8.glb"))
