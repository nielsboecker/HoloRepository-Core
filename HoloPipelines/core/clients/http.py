"""
This module contains provides a generic HTTP client with helper methods for
fetching data from the web.
"""
import io
import os
import logging
from zipfile import ZipFile

import requests
from config import POST_REQUEST_TIMEOUT


def fetch_input_from_url(url_to_zip_file: str) -> bytes:
    """
    Fetches a zipped resource and returns the content.
    :return resource content as bytes
    """
    response = requests.get(url_to_zip_file)
    if response.status_code != 200:
        raise Exception(f"HTTP response {response.status_code}: {response.content}")

    logging.info(f"Download of '{url_to_zip_file}' was successful")
    return response.content


def unzip_file(zipped_data: bytes, output_directory_path: str) -> None:
    """
    Unzips a file to a given directory.
    """
    with ZipFile(io.BytesIO(zipped_data)) as zip_file:
        zip_file.extractall(output_directory_path)
        logging.info(f"Successfully extracted to '{output_directory_path}'")


def download_and_unzip(url_to_zip_file: str, output_directory_path: str) -> None:
    """
    Fetches a zip resource and unpacks it. The zip file itself is only read in-memory.
    """
    input_zip_bytes = fetch_input_from_url(url_to_zip_file)
    unzip_file(input_zip_bytes, output_directory_path)


def post_file(
    model_host: str, model_port: int, input_file_path: str, output_file_path: str
) -> None:
    """
    Calls a pre-trained Niftynet model. The model has to be running and expose the
    /model endpoint, as documented in the /models directory.
    """
    model_endpoint = f"{model_host}:{model_port}/model"

    with open(input_file_path, "rb") as input_file:
        files = {"file": input_file}
        response = requests.post(
            model_endpoint, files=files, timeout=POST_REQUEST_TIMEOUT
        )
        if response.status_code != 200:
            raise Exception(f"HTTP response {response.status_code}: {response.content}")
    with open(output_file_path, "wb") as output_file:
        output_file.write(response.content)


def post_files(
    model_host: str, model_port: int, input_files_path: str, output_file_path: str
) -> None:
    """
    Calls a pre-trained model endpoint. The model has to be running and expose the
    /model endpoint, as documented in the /models directory. This request will
     try to post every file in the specified input path.
    """
    model_endpoint = f"{model_host}:{model_port}/model"

    files = []
    for filename in os.listdir(input_files_path):
        tmp_path = os.path.join(input_files_path, filename)
        files.append(("file[]", open(tmp_path, "rb")))
    response = requests.post(
        model_endpoint, files=files, timeout=POST_REQUEST_TIMEOUT
    )
    if response.status_code != 200:
        raise Exception(f"HTTP response {response.status_code}: {response.content}")
    with open(output_file_path, "wb") as output_file:
        output_file.write(response.content)
