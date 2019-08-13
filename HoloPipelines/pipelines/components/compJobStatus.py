import requests
from datetime import datetime
import pathlib
import logging


def update_status(
    jobID, jobStatus
):  # TODO rename this comp to just http request? and rename this function to updateJobStatus
    pipelineServerURL = "http://localhost:5000/status"
    data = {jobID: {"status": jobStatus, "timestamp": str(datetime.now())}}
    # data = {"jobID": "j0", "status": "hey", "stamp": "2020"}
    response = requests.post(url=pipelineServerURL, json=data)
    returnCode = response.status_code
    logging.info(returnCode)


def send_file_post_request(url, input_file, output_file):
    inputFile = str(pathlib.Path(input_file))
    outputFile = str(pathlib.Path(output_file))
    with open(inputFile, "rb") as f:
        response = requests.post(url, files={inputFile: f})
    file = open(outputFile, "w+")
    file.write(response.content)
    file.close()
    returnCode = response.status_code
    logging.info(returnCode)


def send_get_request(url, request_body):
    response = requests.post(url=url, json=request_body)
    returnCode = response.status_code
    logging.info(returnCode)


if __name__ == "__main__":
    update_status("j0", "hello")  # TODO remove once done testing
    logging.info(
        "You shouldn't be able to run this component directly after we're done testing"
    )  # TODO look at this too pls
