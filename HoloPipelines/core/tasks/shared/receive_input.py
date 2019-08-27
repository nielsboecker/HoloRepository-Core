"""
This module contains the functions that upon starting a pipeline go and
fetch the input imaging studies from a PACS.
"""
from core.clients.http import download_and_unzip


def fetch_and_unzip(imaging_study_endpoint: str, input_directory_path: str) -> None:
    """
    Fetches and unpacks a zipped resource. Input is a DICOM directory stored in a zip.
    """
    download_and_unzip(imaging_study_endpoint, input_directory_path)
