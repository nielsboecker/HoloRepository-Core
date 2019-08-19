import io
import requests
from pathlib import Path
from flask_json import json_response
from zipfile import ZipFile
import logging

input_directory = Path("input")

FORMAT = "%(asctime)-15s -function name:%(funcName)s -%(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)


def fetch_request_input_file(filename, request_input_data_URL):
    this_cwd = Path.cwd()
    response = requests.get(request_input_data_URL)
    if response.status_code != 200:
        return json_response(message="image study endpoint failure", status_code=404)
    file_dir = this_cwd.joinpath(str(input_directory), filename)
    open(file_dir, "wb+").write(response.content)
    logging.debug("file dir: " + str(file_dir))

    filename_unzip = filename.rsplit(".", 1)[0]
    logging.debug("unzip file name:" + filename_unzip)

    # unzip the input file
    file_dir = this_cwd.joinpath(str(input_directory), filename)
    path_to_store_unzip_file = this_cwd.joinpath(str(input_directory), filename_unzip)
    with ZipFile(io.BytesIO(response.content), "r") as zipObj:
        zipObj.extractall(str(path_to_store_unzip_file))
    return str(path_to_store_unzip_file)
