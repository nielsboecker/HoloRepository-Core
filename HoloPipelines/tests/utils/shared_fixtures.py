import os

from pytest import fixture

test_output_path = "./__test_output__"


@fixture
def create_output_directory():
    """
    Creates directory for test output data, if it does not exist yet.
    """
    os.makedirs(test_output_path, exist_ok=True)
