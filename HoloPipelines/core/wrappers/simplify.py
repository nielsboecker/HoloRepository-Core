import logging
import os
import stat
import subprocess

from config import SIMPLIFICATION_RATIO  # TODO acutally add this in config

STAT_OWNER_EXECUTABLE = stat.S_IEXEC

current_script_directory = os.path.dirname(os.path.realpath(__file__))


def call_simplify(
    obj_input_path: str,
    obj_output_path: str,
    simplification_ratio: float = float(SIMPLIFICATION_RATIO),
):
    # NOTE: link to simplify repository https://github.com/sp4cerat/Fast-Quadric-Mesh-Simplification
    simplify_command = [
        "./simplify",
        obj_input_path,
        obj_output_path,
        str(simplification_ratio),
    ]

    os.chmod("simplify", STAT_OWNER_EXECUTABLE)

    completed_process = subprocess.run(simplify_command, cwd=current_script_directory)
    if completed_process.returncode == 0:
        logging.info("simplify wrapper: Simplification succeeded")
    else:
        raise Exception("simplify wrapper: Simplification failed")
