import glob
import os
import pathlib
import logging
import requests
from zipfile import ZipFile


def save_request_file_to_input_dir(filename, request_input_data_URL):
    response = requests.get(request_input_data_URL)
    open(filename, "wb+").write(response.content)
    return filename  # return saved file location


def unzip_the_file(filename):
    with ZipFile(filename, "r") as zipObj:  # unzip
        zipObj.extractall(str(pathlib.Path(filename).parents[0]))
        os.remove(filename)
    directory_list = glob.glob(str(pathlib.Path(filename).parents[0].joinpath("*")))
    return str(directory_list[0])  # return unzipped location


def main(jobID, image_url):
    file_list = [
        str(pathlib.Path.cwd().parents[1].joinpath("jobs")),
        str(pathlib.Path.cwd().parents[1].joinpath("jobs", str(jobID))),
        str(pathlib.Path.cwd().parents[1].joinpath("jobs", str(jobID), "image")),
    ]
    for file_path in file_list:
        if not os.path.exists(file_path):
            os.mkdir(file_path)
    saved_to = save_request_file_to_input_dir(
        str(pathlib.Path(file_list[-1]).joinpath("temp.zip")), image_url
    )
    return unzip_the_file(saved_to)


if __name__ == "__main__":
    logging.error("component can't run on it's own")
