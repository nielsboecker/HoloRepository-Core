"""
This module provides a wrapper around the simplify binary, which can be used
in the pipelines to reduce the file size of OBJ files significantly.

Currently, this component is unused, as it caused a strange inference effect
when used in conjuntion with obj2gltf in the tool-chain. We conducted a more
in-depth analysis in issue #97. In short, we believe that the intermediate OBJ
files are inverted / have a wrong coordinate system. However, the issue will
not be visible if these OBJ files are converted to GLB directly. It only shows
when the OBJ is first simplified; in this case, the faces seem to be inverted.

We disabled the step for now. Just by converting OBJ to GLB, acceptable file
sizes of aroun 4 to 6 MB are achieved. Future work could analyse the issue
further and re-enable the simplification step for each pipeline.
"""
import logging
import subprocess

from config import SIMPLIFICATION_RATIO

simplify_binary_path = "./core/third_party/fast_quadric_mesh_simplification/simplify"


def call_simplify(
    obj_input_file_path: str,
    obj_output_file_path: str,
    simplification_ratio: float = SIMPLIFICATION_RATIO,
):
    simplify_command = [
        simplify_binary_path,
        obj_input_file_path,
        obj_output_file_path,
        str(simplification_ratio),
    ]

    completed_process = subprocess.run(simplify_command)
    if completed_process.returncode == 0:
        logging.info("simplify wrapper: Simplification succeeded")
    else:
        raise Exception("simplify wrapper: Simplification failed")
