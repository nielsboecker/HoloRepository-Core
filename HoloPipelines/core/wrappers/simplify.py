"""
Currently, this component is unused, Because when the 3D model goes though the simplify process
the output looks weird. It seems like the textures outside are transparent,
and only on the inside of surfaces, are visible
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
