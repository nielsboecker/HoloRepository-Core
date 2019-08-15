import glob
import os
import io
import pathlib
import logging
import requests
from zipfile import ZipFile

this_comp_path = str(pathlib.Path(str(os.path.dirname(os.path.realpath(__file__)))))


def get_content_from_url(request_input_data_URL):
    response = requests.get(request_input_data_URL)
    return response.content


def unzip_the_file(zipped_data, save_dest):
    with ZipFile(io.BytesIO(zipped_data)) as zipObj:  # unzip
        zipObj.extractall(str(pathlib.Path(save_dest)))
    directory_list = glob.glob(str(pathlib.Path(save_dest).parents[0].joinpath("*")))
    return str(directory_list[0])  # return unzipped location


def main(jobID, image_url):
    file_list = [
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


if __name__ == "__main__":
    logging.error("component can't run on it's own")
