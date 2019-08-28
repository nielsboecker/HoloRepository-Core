"""
This module contains provides a generic HTTP client with helper methods for
fetching data from the web.
"""
import io
import logging
from zipfile import ZipFile

import requests


def download_and_unzip(url_to_zip_file: str, output_directory_path: str) -> None:
    """
    Fetches a zip resource and unpacks it. The zip file itself is only read in-memory.
    """
    response = requests.get(url_to_zip_file)
    logging.info(f"Download of '{url_to_zip_file}' was successful")

    with ZipFile(io.BytesIO(response.content)) as zip_file:
        zip_file.extractall(output_directory_path)
        logging.info(f"Successfully extracted to '{output_directory_path}'")
