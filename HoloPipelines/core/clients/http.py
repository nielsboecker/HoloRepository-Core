"""
This module contains provides a generic HTTP client with helper methods for
fetching data from the web.
"""
import io
import logging
from zipfile import ZipFile

import requests


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
