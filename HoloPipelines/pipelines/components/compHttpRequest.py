import requests
import pathlib
import sys


def sendFilePostRequest(url, inputFile, outputFile):
    inputFile = str(pathlib.Path(inputFile))
    outputFile = str(pathlib.Path(outputFile))
    with open(inputFile, "rb") as inputFileData:
        file = {"file": inputFileData}
        try:
            response = requests.post(url, files=file, timeout=10)
        except Exception:
            sys.exit(
                "compHttpReuest: an error happened in a POST reuqest, this might be due to timeout or bad request. Or if this is a request to one of the segmentation model, then please make sure the container with the model is running."
            )
    with open(outputFile, "wb") as file:
        file.write(response.content)
    return outputFile


if __name__ == "__main__":
    print("component can't run on its own")
