import os
import shutil

from pytest import fixture

test_output_directory_path = "./__test_output__"
test_input_directory_path = "./__test_output__"


@fixture
def create_output_directory():
    """
    Creates directory for test output data, if it does not exist yet.
    """
    os.makedirs(test_output_directory_path, exist_ok=True)


@fixture
def create_input_directory():
    """
    Creates directory for test input data, if it does not exist yet.
    """
    os.makedirs(test_input_directory_path, exist_ok=True)


@fixture(scope="session", autouse=True)
def create_and_delete_test_output_directory():
    """
    Creates test output directory before first test in session, and deletes it after
    the last test ran.
    """
    os.makedirs(test_output_directory_path, exist_ok=True)
    yield

    shutil.rmtree(test_output_directory_path)
