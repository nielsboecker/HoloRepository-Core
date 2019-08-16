import requests
import pathlib
import logging
import os
import json


FORMAT = "%(asctime)-15s -function name:%(funcName)s -%(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)


def send_file_post_request(url, input_file, output_file):
    input_file = str(pathlib.Path(input_file))
    output_file = str(pathlib.Path(output_file))
    with open(input_file, "rb") as input_file:
        in_file = {"file": input_file}
    input_file.close()
    response = requests.post(url, files=in_file)
    with open(output_file, "wb") as output_file:
        output_file.write(response.content)
    output_file.close()
    logging.debug("return code: " + response.status_code)
    return output_file


def send_post_to_status(json_data):
    if str(os.environ.get("SEVER_URL")) != "None":
        json_data = requests.post(str(os.environ.get("SEVER_URL")), json=json_data)
        return json_data
    else:
        logging.debug("json_data: " + json.dumps(json_data))
        response = requests.post("http://localhost:3100/api/v1/status", json=json_data)
        return response


if __name__ == "__main__":
    print("component can't run on its own")
