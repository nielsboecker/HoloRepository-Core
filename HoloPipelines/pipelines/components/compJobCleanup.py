import pathlib
import shutil
import os
import logging

this_comp_path = str(pathlib.Path(str(os.path.dirname(os.path.realpath(__file__)))))


def main(jobID):
    if os.path.exists(
        str(pathlib.Path(this_comp_path).parents[1].joinpath("jobs", str(jobID)))
    ):
        shutil.rmtree(
            str(pathlib.Path(this_comp_path).parents[1].joinpath("jobs", str(jobID)))
        )


if __name__ == "__main__":
    logging.error("component can't run on its own")
