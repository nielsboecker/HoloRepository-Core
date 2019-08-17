from datetime import datetime
from os import path
import requests
import pathlib
import json

# TODO: split this up between http client (for technical stuff), dispatch_output

# TODO: Refactor next lines
def send_file_request_to_accessor(meta_data):
    output_file_dir = str(pathlib.Path(meta_data["outputFileDir"]))
    size_of_output_file = str(path.getsize(output_file_dir) / 1024)
    # get the pipelinelist json file
    print(meta_data["author"]["aid"])

    # manipulate author data
    author_for_accessor = {
        "aid": meta_data["author"]["aid"],
        "name": meta_data["author"]["name"],
    }

    # manipulate patient data
    patient_for_accessor = {
        "pid": meta_data["patient"]["pid"],
        "name": meta_data["patient"]["name"],
    }

    request_body = {
        "title": meta_data["title"],
        "description": meta_data["description"],
        "contentType": "model/gltf-binary",
        "fileSizeInKb": size_of_output_file,
        "bodySite": meta_data["bodySite"],
        "dateOfImaging": meta_data["dateOfImaging"],
        "creationDate": meta_data["creationDate"],
        "creationMode": "GENERATE_FROM_IMAGING_STUDY",
        "creationDescription": meta_data["creationDescription"],
        "author": json.dumps(author_for_accessor),
        "patient": json.dumps(patient_for_accessor),
    }
    files = {"hologramFile": open(output_file_dir, "rb")}
    print(request_body)
    response = requests.post(
        # TODO: Should not be hard-coded in here
        "http://localhost:3200/api/v1/holograms", data=request_body, files=files
    )
    print(response.content)
    return_code = response.status_code
    print(return_code)
    return request_body


# TODO: Refactor
def add_info_for_accesor(infoForAccessor, title, creationDes, outputDir):

    infoForAccessor.update(
        {
            "title": title,
            "creationDate": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "creationDescription": creationDes,
            "outputFileDir": outputDir,
        }
    )
    print("info: " + json.dumps(infoForAccessor))

    return infoForAccessor