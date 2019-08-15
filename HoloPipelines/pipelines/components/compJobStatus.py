import requests
from datetime import datetime
import pathlib


def update_status(
    job_ID, job_status
):  # TODO rename this comp to just http request? and rename this function to updateJobStatus
    pipeline_server_URL = "http://localhost:5000/api/v1/status"
    data = {job_ID: {"status": job_status, "timestamp": str(datetime.now())}}
    # data = {"jobID": "j0", "status": "hey", "stamp": "2020"}
    response = requests.post(url=pipeline_server_URL, json=data)
    return_code = response.status_code
    print(return_code)


def send_file_post_request(url, input_file, outputFile):
    input_file = str(pathlib.Path(input_file))
    outputFile = str(pathlib.Path(outputFile))
    with open(input_file, "rb") as f:
        response = requests.post(url, files={input_file: f})
    file = open(outputFile, "w+")
    file.write(response.content)
    file.close()
    return_code = response.status_code
    print(return_code)


if __name__ == "__main__":
    update_status("j0", "hello")  # TODO remove once done testing
    print(
        "You shouldn't be able to run this component directly after we're done testing"
    )  # TODO look at this too pls
