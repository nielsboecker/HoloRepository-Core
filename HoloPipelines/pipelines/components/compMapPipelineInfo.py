import os.path
import json


def map_pipelines_info():

    pipeline_dict = {}
    with open(os.path.dirname(__file__) + "/../../pipelineList.json") as json_file:
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
