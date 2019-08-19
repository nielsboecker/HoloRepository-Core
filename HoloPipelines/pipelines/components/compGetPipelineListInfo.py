import pathlib
import os
import json


def get_pipeline_list():
    new_cwd = str(pathlib.Path(str(os.path.dirname(os.path.realpath(__file__)))))
    configFileName = "pipelineList.json"

    with open(
        str(pathlib.Path(new_cwd).parents[1].joinpath(str(configFileName)))
    ) as json_file:
        list_of_pipeline = json.load(json_file)
    json_file.close()
    return list_of_pipeline
