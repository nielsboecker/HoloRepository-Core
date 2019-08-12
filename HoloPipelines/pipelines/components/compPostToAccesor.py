from os import path
import requests
import pathlib
import json


def send_file_post_request_to_accessor(
    title,
    outputFileDir,
    description,
    bodySite,
    dateOfImaging,
    creationDate,
    creationDescription,
    author,
    patient,
):
    outputFileDir = str(pathlib.Path(outputFileDir))
    sizeOfOutputFile = str(path.getsize(outputFileDir) / 1000)
    # print("file: "+str(file)
    # get the pipelinelist json file

    # manipulate author data
    authorForAccessor = {"aid": author["aid"], "name": author["name"]}

    # manipulate patient data
    patientForAccessor = {"pid": patient["pid"], "name": patient["name"]}

    requestBody = {
        "title": title,
        "description": description,
        "contentType": "model/gltf-binary",
        "fileSizeInKb": sizeOfOutputFile,
        "bodySite": bodySite,
        "dateOfImaging": dateOfImaging,
        "creationDate": creationDate,
        "creationMode": "GENERATE_FROM_IMAGING_STUDY",
        "creationDescription": creationDescription,
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
