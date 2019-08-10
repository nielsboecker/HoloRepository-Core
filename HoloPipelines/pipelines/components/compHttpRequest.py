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


if __name__ == "__main__":
    print("component can't run on its own")
