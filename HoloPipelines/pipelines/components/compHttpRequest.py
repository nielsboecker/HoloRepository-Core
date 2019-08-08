import requests
import pathlib


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


def sendFilePostRequestToAccessor(url, outputFileDir):
    hologramFile = str(pathlib.Path(outputFileDir))
    file = {"file": open(hologramFile, "rb")}
    # requestBody = {"title": ""}
    response = requests.post(url, files=file)

    returnCode = response.status_code
    print(returnCode)
    return hologramFile


if __name__ == "__main__":
    print("component can't run on its own")
