import os
from typing import Any

from core.wrappers import simplify
from .utils.shared_fixtures import (
    test_output_directory_path,
    create_and_delete_test_output_directory,
)

test_obj_file_path = "tests/utils/teddy.obj"
test_output_obj_file_path = f"{test_output_directory_path}/simplifed_teddy.obj"


def test_simplify_call_default(create_and_delete_test_output_directory: Any):
    simplify.call_simplify(test_obj_file_path, test_output_obj_file_path)
    assert os.path.exists(test_output_obj_file_path)


def test_simplify_call_03(create_and_delete_test_output_directory: Any):
    simplify.call_simplify(test_obj_file_path, test_output_obj_file_path, 0.3)
    assert os.path.exists(test_output_obj_file_path)
