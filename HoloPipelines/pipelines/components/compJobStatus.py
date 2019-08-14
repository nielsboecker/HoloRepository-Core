import requests
from datetime import datetime
import pathlib


def update_status(
    jobID, jobStatus
):  # TODO rename this comp to just http request? and rename this function to updateJobStatus
    pipelineServerURL = "http://localhost:5000/api/v1/status"
    data = {jobID: {"status": jobStatus, "timestamp": str(datetime.now())}}
    # data = {"jobID": "j0", "status": "hey", "stamp": "2020"}
    response = requests.post(url=pipelineServerURL, json=data)
    returnCode = response.status_code
    print(returnCode)


def send_file_post_request(url, inputFile, outputFile):
    inputFile = str(pathlib.Path(inputFile))
    outputFile = str(pathlib.Path(outputFile))
    with open(inputFile, "rb") as f:
        response = requests.post(url, files={inputFile: f})
    file = open(outputFile, "w+")
    file.write(response.content)
    file.close()
    returnCode = response.status_code
    print(returnCode)


if __name__ == "__main__":
    update_status("j0", "hello")  # TODO remove once done testing
    print(
        "You shouldn't be able to run this component directly after we're done testing"
    )  # TODO look at this too pls
