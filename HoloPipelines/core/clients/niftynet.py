import requests


def call_model(
    model_host: str, model_port: int, input_file_path: str, output_file_path: str
):
    """
    Calls a pre-trained Niftynet model. The model has to be running and expose the
    /model endpoint, as documented in the /models directory.
    """
    model_endpoint = f"{model_host}:{model_port}/model"

    with open(input_file_path, "rb") as input_fie:
        files = {"file": input_fie}
        response = requests.post(model_endpoint, files=files, timeout=10)
        if response.status_code != 200:
            raise Exception(f"HTTP Response {response.status_code}: {response.content}")
    with open(output_file_path, "wb") as output_file:
        output_file.write(response.content)
