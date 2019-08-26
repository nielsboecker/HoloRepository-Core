"""
This module contains functionality related to communicating with pre-trained neural
networks built with Niftynet and packaged for HoloPipelines usage as described in
the /models/README. Models have a well-defined API and this module is the counterpart
that calls this API and thus integrates it with the pipelines.
"""

import requests

from config import NIFTYNET_MODEL_TIMEOUT


def call_model(
    model_host: str, model_port: int, input_file_path: str, output_file_path: str
) -> None:
    """
    Calls a pre-trained Niftynet model. The model has to be running and expose the
    /model endpoint, as documented in the /models directory.
    """
    model_endpoint = f"{model_host}:{model_port}/model"

    with open(input_file_path, "rb") as input_fie:
        files = {"file": input_fie}
        response = requests.post(
            model_endpoint, files=files, timeout=NIFTYNET_MODEL_TIMEOUT
        )
        if response.status_code != 200:
            raise Exception(f"HTTP response {response.status_code}: {response.content}")
    with open(output_file_path, "wb") as output_file:
        output_file.write(response.content)
