from os import path
import requests
import pathlib
import json


def send_file_request_to_accessor(info_for_accessor):
    output_file_dir = str(pathlib.Path(info_for_accessor["outputFileDir"]))
    size_of_output_file = str(path.getsize(output_file_dir) / 1000)
    # print("file: "+str(file)
    # get the pipelinelist json file
    print(info_for_accessor["author"]["aid"])

    # manipulate author data
    author_for_accessor = {
        "aid": info_for_accessor["author"]["aid"],
        "name": info_for_accessor["author"]["name"],
    }

    # manipulate patient data
    patient_for_accessor = {
        "pid": info_for_accessor["patient"]["pid"],
        "name": info_for_accessor["patient"]["name"],
    }

    request_body = {
        "title": info_for_accessor["title"],
        "description": info_for_accessor["description"],
        "contentType": "model/gltf-binary",
        "fileSizeInKb": size_of_output_file,
        "bodySite": info_for_accessor["bodySite"],
        "dateOfImaging": info_for_accessor["dateOfImaging"],
        "creationDate": info_for_accessor["creationDate"],
        "creationMode": "GENERATE_FROM_IMAGING_STUDY",
        "creationDescription": info_for_accessor["creationDescription"],
        "author": json.dumps(author_for_accessor),
        "patient": json.dumps(patient_for_accessor),
    }
    files = {"hologramFile": open(output_file_dir, "rb")}
    print(request_body)
    response = requests.post(
        "http://localhost:3200/api/v1/holograms", data=request_body, files=files
    )
    print(response.content)
    return_code = response.status_code
    print(return_code)
    return request_body


if __name__ == "__main__":
    print("component can't run on its own")
