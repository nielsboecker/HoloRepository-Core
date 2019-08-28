import os

import pytest
from pip._vendor.distlib._backport import shutil

test_output_directory_path = "__test_output__"


@pytest.fixture(scope="session", autouse=True)
def create_and_delete_test_output_directory():
    """
    Creates test output directory before first test in session, and deletes it after
    the last test ran.
    """
    os.makedirs(test_output_directory_path, exist_ok=True)
    yield

    shutil.rmtree(test_output_directory_path)
