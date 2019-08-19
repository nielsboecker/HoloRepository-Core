import requests
import pathlib
import sys
import logging
import os
import json

FORMAT = "%(asctime)-15s -function name:%(funcName)s -%(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)


def send_file_post_request(url, inputFile, outputFile):
    inputFile = str(pathlib.Path(inputFile))
    outputFile = str(pathlib.Path(outputFile))
    with open(inputFile, "rb") as inputFileData:
        fileToSend = {"file": inputFileData}
        try:
            response = requests.post(url, files=fileToSend, timeout=10)
            if response.status_code != 200:
                # status 400 with "No file in the request" or "No selected file"
                sys.exit(
                    "compHttpRequest: error, bad status code (got {}: {})".format(
                        response.status_code, response.content
                    )
                )
        except Exception:
            sys.exit(
                "compHttpRequest: an error happened in a POST request, this might be due to timeout or bad request. Or if this is a request to one of the segmentation model, then please make sure the container with the model is running."
            )
    with open(outputFile, "wb") as fileToWrite:
        fileToWrite.write(response.content)
    return outputFile


def send_post_to_status(json_data):
    if str(os.environ.get("SEVER_URL")) != "None":
        json_data = requests.post(str(os.environ.get("SEVER_URL")), json=json_data)
        return json_data
    else:
        logging.debug("json_data: " + json.dumps(json_data))
        # TODO: Don't hard-code that here
        response = requests.post("http://localhost:3100/api/v1/status", json=json_data)
        return response


if __name__ == "__main__":
    logging.error("component can't run on its own")
