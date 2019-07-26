import requests
from datetime import datetime
import json


def updateStatus(jobID, jobStatus):
    pipelineServerURL = "http://localhost:5000/status"
    data = {jobID: {"status": jobStatus, "timestamp": str(datetime.now())}}
    # data = {"jobID": "j0", "status": "hey", "stamp": "2020"}
    sendRequest = requests.post(url=pipelineServerURL, json=data)
    pastebinURL = sendRequest.text
    returnCode = sendRequest.status_code
    print(returnCode)


if __name__ == "__main__":
    updateStatus("j0", "goFkYoSelf")
    print("fdshfjksd")
