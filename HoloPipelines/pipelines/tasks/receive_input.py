import glob
import os
import io
import pathlib
import logging
import requests
from zipfile import ZipFile
from pathlib import Path
from flask_json import json_response

this_comp_path = str(pathlib.Path(str(os.path.dirname(os.path.realpath(__file__)))))


def get_content_from_url(request_input_data_URL):
    response = requests.get(request_input_data_URL)
    return response.content


def unzip_the_file(zipped_data, save_dest):
    with ZipFile(io.BytesIO(zipped_data)) as zipObj:  # unzip
        zipObj.extractall(str(pathlib.Path(save_dest)))
    directory_list = glob.glob(str(pathlib.Path(save_dest).parents[0].joinpath("*")))
    return str(directory_list[0])  # return unzipped location


def fetch_and_unzip(jobID, image_url):
    logging.info("Fetching " + image_url)
    file_list = [
        # TODO: Refactor this
        str(pathlib.Path(this_comp_path).parents[1].joinpath("jobs")),
        str(pathlib.Path(this_comp_path).parents[1].joinpath("jobs", str(jobID))),
        str(
            pathlib.Path(this_comp_path)
            .parents[1]
            .joinpath("jobs", str(jobID), "image")
        ),
    ]
    for file_path in file_list:
        if not os.path.exists(file_path):
            os.mkdir(file_path)
    download_content = get_content_from_url(image_url)
    return unzip_the_file(download_content, str(pathlib.Path(file_list[-1])))


# TODO: This was an unused method in compGetInput.py (which itself was unused).
#  Sort out if this does anything different from the above method
input_directory = Path("input")
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
