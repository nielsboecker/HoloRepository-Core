import requests
from datetime import datetime
import pathlib


def updateStatus(
    jobID, jobStatus
):  # TODO rename this comp to just http request? and rename this function to updateJobStatus
    pipelineServerURL = "http://localhost:5000/status"
    data = {jobID: {"status": jobStatus, "timestamp": str(datetime.now())}}
    # data = {"jobID": "j0", "status": "hey", "stamp": "2020"}
    response = requests.post(url=pipelineServerURL, json=data)
    returnCode = response.status_code
    print(returnCode)


def sendFilePostRequest(url, inputFile, outputFile):
    inputFile = str(pathlib.Path(inputFile))
    outputFile = str(pathlib.Path(outputFile))
    file = {"file": open(inputFile, "rb")}
    response = requests.post(url, files=file)
    file = open(outputFile, "wb")
    file.write(response.content)
    file.close()
    returnCode = response.status_code
    print(returnCode)
    return outputFile


def sendGetRequest(url, requestBody):
    response = requests.post(url=url, json=requestBody)
    returnCode = response.status_code
    print(returnCode)


if __name__ == "__main__":
    updateStatus("j0", "hello")  # TODO remove once done testing
    print(
        "You shouldn't be able to run this component directly after we're done testing"
    )  # TODO look at this too pls
