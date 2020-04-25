"""
This module contains helper functions to show infos about pipelines
and load them dynamically.
"""

import importlib
import json
import logging
from typing import Any


def get_models_dict() -> dict:
    """
    :return: dict of available pipelines representing "pipelines.json"
    """
    with open("./models.json", "r") as models_file:
        return json.load(models_file)


def get_models_ids_list() -> list:
    """
    :return: list of the ids of available pipelines according to "pipelines.json"
    """
    return list(get_models_dict().keys())


def get_model_dict(modelname: str) -> dict:
    """
    :param modelname: Name of the model as written in models.json
    :return: dict containing the dictionairy for the specified model
    """
    return get_models_dict()[modelname]
