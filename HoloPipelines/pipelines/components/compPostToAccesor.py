from os import path
import requests
import pathlib
import json


def sendFilePostRequestToAccessor(infoForAccesor):
    outputFileDir = str(pathlib.Path(infoForAccesor["outputFileDir"]))
    sizeOfOutputFile = str(path.getsize(outputFileDir) / 1000)
    # print("file: "+str(file)
    # get the pipelinelist json file
    print(infoForAccesor["author"]["aid"])

    # manipulate author data
    authorForAccessor = {
        "aid": infoForAccesor["author"]["aid"],
        "name": infoForAccesor["author"]["name"],
    }

    # manipulate patient data
    patientForAccessor = {
        "pid": infoForAccesor["patient"]["pid"],
        "name": infoForAccesor["patient"]["name"],
    }

    requestBody = {
        "title": infoForAccesor["title"],
        "description": infoForAccesor["description"],
        "contentType": "model/gltf-binary",
        "fileSizeInKb": sizeOfOutputFile,
        "bodySite": infoForAccesor["bodySite"],
        "dateOfImaging": infoForAccesor["dateOfImaging"],
        "creationDate": infoForAccesor["creationDate"],
        "creationMode": "GENERATE_FROM_IMAGING_STUDY",
        "creationDescription": infoForAccesor["creationDescription"],
        "author": json.dumps(authorForAccessor),
        "patient": json.dumps(patientForAccessor),
    }
    files = {"hologramFile": open(outputFileDir, "rb")}
    print(requestBody)
    response = requests.post(
        "http://localhost:3200/api/v1/holograms", data=requestBody, files=files
    )
    print(response.content)
    returnCode = response.status_code
    print(returnCode)
    return requestBody


if __name__ == "__main__":
    print("component can't run on its own")
