import requests
import pathlib
import sys
import logging

logging.basicConfig(level=logging.INFO)


def sendFilePostRequest(url, inputFile, outputFile):
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


if __name__ == "__main__":
    logging.error("component can't run on its own")
