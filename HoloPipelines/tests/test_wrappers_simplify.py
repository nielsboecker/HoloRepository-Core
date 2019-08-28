import os
import sys
import pytest

sys.path.insert(1, os.path.join(sys.path[0], ".."))  # noqa
from core.wrappers import simplify

this_test_name = os.path.basename(__file__).replace(".py", "")

test_obj_file_path = "/tests/utils/teddy.obj"
test_output_obj_file_path = "/tests/utils/simplifed_teddy.obj"


@pytest.fixture
def output_obj_cleanup():
    if os.path.exists(test_output_obj_file_path):
        os.remove(test_output_obj_file_path)

    yield

    if os.path.exists(test_output_obj_file_path):
        os.remove(test_output_obj_file_path)


def test_simplify_call_default(output_obj_cleanup):
    simplify.call_simplify(test_obj_file_path, test_output_obj_file_path)
    assert os.path.exists(test_output_obj_file_path)


def test_simplify_call_03(output_obj_cleanup):
    simplify.call_simplify(test_obj_file_path, test_output_obj_file_path, 0.3)
    assert os.path.exists(test_output_obj_file_path)
