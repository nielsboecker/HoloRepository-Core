import logging
import os
import shutil
import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from zipfile import ZipFile

# from core.pipelines.pipelines_controller import load_pipeline_dynamically
from jobs.jobs_controller import create_random_job_id

# from jobs.jobs_io import (
#     create_directory_for_job,
#     remove_directory_for_job,
#     get_logger_for_job,
# )
import pytest
import requests

# import json
# import pathlib

pythonPath = sys.executable
zipFileName = "__temp__.zip"
segmentedAbdomenFileName = "__segmentedAbdomen__.nii.gz"
lung_pipeline_job_id = create_random_job_id()
abdominal_pipeline_job_id = create_random_job_id()

test_input_path = "__test_input__"
dicomPath = f"{test_input_path}/dicom"
niftiPath = f"{test_input_path}/nifti"

test_output_path = "__test_output__"
objPath = f"{test_output_path}/obj"
glbPath = f"{test_output_path}/glb"


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
        f"{dicomPath}/3_Axial_CE": [
            "https://holoblob.blob.core.windows.net/test/3_Axial_CE.zip",
            str(dicomPath),
        ],
        f"{dicomPath}/abdomen": [
            "https://holoblob.blob.core.windows.net/mock-pacs/abdomen.zip",
            str(dicomPath),
        ],
        f"{dicomPath}/1103_3_glm.nii": [
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
            open(f"{test_input_path}/{zipFileName}", "wb+").write(response.content)

            logging.info("Decompressing...")
            with ZipFile(zipFileName, "r") as zipObj:  # unzip
                zipObj.extractall(saveTo)
            os.remove(zipFileName)

    # download data for mock server (not in loop above as this one does not come in zip)
    if not os.path.exists(f"{niftiPath}/{segmentedAbdomenFileName}"):
        urlNiftyOut = "https://holoblob.blob.core.windows.net/mock-pacs/Owenpap___niftynet_out.nii.gz"
        response = requests.get(urlNiftyOut)
        open(f"{niftiPath}/{segmentedAbdomenFileName}", "wb+").write(response.content)

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
        f"{glbPath}/testResult0.glb",
        f"{glbPath}/testResult1.glb",
        f"{glbPath}/testResult2.obj",
        f"{glbPath}/testResult3.glb",
        f"{glbPath}/testResult4.glb",
        f"{glbPath}/organNo1.glb",
        f"{glbPath}/organNo2.glb",
        f"{glbPath}/organNo3.glb",
        f"{glbPath}/organNo4.glb",
        f"{glbPath}/organNo5.glb",
        f"{glbPath}/organNo6.glb",
        f"{glbPath}/organNo7.glb",
        f"{glbPath}/organNo8.glb",
    ]

    for meshFileName in generatedMeshList:
        if os.path.exists(meshFileName):
            os.remove(meshFileName)


# FIXME: Fix this tests. It is completely outdated, as the commponent now downloads and posts stuff
# def test_lung_pipelines():
#     test_lung_pipeline_json=pathlib.Path(__file__).parent.joinpath('test_lung_pipeline.json')
#     with open(test_lung_pipeline_json) as json_file:
#         request = json.load(json_file)
#     create_directory_for_job(lung_pipeline_job_id)
#     pipeline_module = load_pipeline_dynamically("lung_segmentation")
#     result = pipeline_module.run(lung_pipeline_job_id, request["imagingStudyEndpoint"], request["medicalData"])
#     assert result


#
# def test_abdominal_pipelines():
#     os.makedirs( f"./__jobs__/{lung_pipeline_job_id}", exist_ok=True)
#     test_abdominal_pipeline_json = pathlib.Path(__file__).parent.joinpath('test_abdominal_pipeline.json')
#     with open(test_abdominal_pipeline_json) as json_file:
#         request = json.load(json_file)
#
#     pipeline_module = load_pipeline_dynamically("abdominal_organs_segmentation")
#     result = pipeline_module.run(lung_pipeline_job_id, request["imagingStudyEndpoint"], request["medicalData"])
#     assert result


# def pytest_sessionfinish(session, exitstatus):
#     remove_directory_for_job(lung_pipeline_job_id)
#     remove_directory_for_job(abdominal_pipeline_job_id)

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
