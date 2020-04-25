"""
This module contains helper functions to show infos about pipelines
and load them dynamically.
"""

import importlib
import json
import logging
from typing import Any


def get_pipelines_dict() -> dict:
    """
    :return: dict of available pipelines representing "pipelines.json"
    """
    with open("./core/pipelines/pipelines.json", "r") as pipelines_file:
        return json.load(pipelines_file)


def get_pipelines_ids_list() -> list:
    """
    :return: list of the ids of available pipelines according to "pipelines.json"
    """
    return list(get_pipelines_dict().keys())


def load_pipeline_dynamically(plid: str) -> Any:
    """
    Loads and returns a pipeline module dynamically, which can then be invoked by its
    run function.
    """
    pl_package_name = f"core.pipelines.{plid}"
    logging.info(f"Importing pipeline package {pl_package_name}")
    return importlib.import_module(pl_package_name)
