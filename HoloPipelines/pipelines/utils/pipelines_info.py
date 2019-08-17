import os
import os.path
import json

# TODO: Refactor or delete
import pathlib


# TODO: From compMapPipelineInfo.py, needs refactoring
def map_pipelines_info():

    pipeline_dict = {}
    with open(os.path.dirname(__file__) + "/../../../pipelineList.json") as json_file:
        pipeline_list = json.load(json_file)
    json_file.close()

    components_list = [
        "plid",
        "title",
        "description",
        "inputConstraints",
        "inputExampleImageUrl",
        "outputExampleImageUrl",
    ]
    pipeline_list_keys = list(pipeline_list.keys())
    pipeline_dict = {
        plid: {
            component: pipeline_list[plid][component] for component in components_list
        }
        for plid in pipeline_list_keys
    }

    return pipeline_dict


# TODO: From compGetPipelineListInfo.py, needs refactoring
def get_pipeline_list():
    new_cwd = str(pathlib.Path(str(os.path.dirname(os.path.realpath(__file__)))))
    configFileName = "pipelineList.json"

    with open(
        str(pathlib.Path(new_cwd).parents[1].joinpath(str(configFileName)))
    ) as json_file:
        list_of_pipeline = json.load(json_file)
    json_file.close()
    return list_of_pipeline