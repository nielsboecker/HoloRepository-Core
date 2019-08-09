import requests
import pathlib
import json
from pathlib import Path
from os import path

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


def sendFilePostRequestToAccessor(title,url, outputFileDir,description,bodySite,dateOfImaging,creationDate,creationDescription,author,patient):
    outputFileDir = str(pathlib.Path(outputFileDir))
    sizeOfOutputFile=str(path.getsize(outputFileDir)/1000)
    file = {"file": open(outputFileDir, "rb")}
    #print("file: "+str(file)
    # get the pipelinelist json file
    this_cwd = pathlib.Path.cwd()
    pipelineListjson=Path("pipelineList.json")
    pipelineListjsonDir=str(this_cwd.parents[1].joinpath(pipelineListjson))
    with open(pipelineListjsonDir) as json_file:
        lsPipe = json.load(json_file)
    json_file.close()
    print(lsPipe)

    # manipulate author data
    authorForAccessor={
        "aid": author["aid"],
        "name": author["name"]
    }

    # manipulate patient data
    patientForAccessor={
        "pid": patient["pid"],
        "name": patient["name"]
    }


    requestBody = {
        "title": title,
        "description": description,
        "contentType": "model/gltf-binary",
        "fileSizeInKb": sizeOfOutputFile,
        "bodySite": bodySite,
        "dateOfImaging":dateOfImaging,
        "creationDate":creationDate,
        "creationMode": "GENERATE_FROM_IMAGING_STUDY",
        "creationDescription":creationDescription,
        "hologramFile":[file],
        "author": authorForAccessor,
        "patient": patientForAccessor

        }
    response = requests.post(url, data=requestBody)

    returnCode = response.status_code
    print(returnCode)
    return requestBody





if __name__ == "__main__":
    print("component can't run on its own")
