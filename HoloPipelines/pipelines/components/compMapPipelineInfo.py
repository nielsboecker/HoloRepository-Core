import os.path
import json


def map_pipelines_info():

    pipeline_dict = {}
    with open(os.path.dirname(__file__) + "/../../pipelineList.json") as json_file:
        pipeline_list = json.load(json_file)
    json_file.close()

    for (plid, pipeline) in pipeline_list.items():
        pipeline_dict[plid] = {
            "plid": plid,
            "title": pipeline["title"],
            "description": pipeline["description"],
            "inputConstraints": pipeline["inputConstraints"],
            "inputExampleImageUrl": pipeline["inputExampleImageUrl"],
            "outputExampleImageUrl": pipeline["outputExampleImageUrl"],
        }
    return pipeline_dict
