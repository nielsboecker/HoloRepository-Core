# TODO: This is only used in adminal pipeline. Use an adapter for that and have a more generic http client

import pathlib
import sys

import requests


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
