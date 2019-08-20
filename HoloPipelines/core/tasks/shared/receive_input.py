import io
from zipfile import ZipFile

import requests


def fetch_input_from_url(url: str):
    """
    Fetches and returns a resource.
    """
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"HTTP response {response.status_code}: {response.content}")
    return response.content


def unzip_file(zipped_data: bytes, output_directory: str):
    """
    Unzips a file to a given directory.
    """
    with ZipFile(io.BytesIO(zipped_data)) as zipped_file:
        zipped_file.extractall(output_directory)


def fetch_and_unzip(imaging_study_endpoint: str, input_directory_path: str):
    """
    Fetches and unpacks a zipped resource. Input is a DICOM directory stored in a
    zip. Notice how the resource is kept in-memory prior to unzipping.
    """
    input_zip = fetch_input_from_url(imaging_study_endpoint)
    unzip_file(input_zip, input_directory_path)
