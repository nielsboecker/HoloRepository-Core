import json
from os import path

# TODO: Refactor or delete
import pathlib


def read_and_map_pipelines_info():
    with open("./core/pipelines/pipelines_list.json") as pipelines_list_file:
        pipelines_list = json.load(pipelines_list_file)

    required_keys = [
        "plid",
        "title",
        "description",
        "inputConstraints",
        "inputExampleImageUrl",
        "outputExampleImageUrl",
    ]

    # Remove fields that are just for internal use (may be refactored as actually there
    # is not necessarily the need to have more fields internally than externally)
    return {
        plid: {key: pipelines_list[plid][key] for key in required_keys}
        for plid in (list(pipelines_list.keys()))
    }


# TODO: From compGetPipelineListInfo.py, needs refactoring
def get_pipeline_list():
    new_cwd = str(pathlib.Path(str(path.dirname(path.realpath(__file__)))))
    configFileName = "./core/pipelines/pipelines_list.json"

    with open(
        str(pathlib.Path(new_cwd).parents[1].joinpath(str(configFileName)))
    ) as json_file:
        list_of_pipeline = json.load(json_file)
    json_file.close()
    return list_of_pipeline
