import requests
import pathlib
import logging

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
    returnCode = response.status_code
    logging.debug("return code: " + returnCode)
    return output_file


if __name__ == "__main__":
    print("component can't run on its own")
