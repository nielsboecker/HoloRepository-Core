import requests
import pathlib
import logging


def send_file_post_request(url, input_file, output_file):
    inputFile = str(pathlib.Path(input_file))
    outputFile = str(pathlib.Path(output_file))
    file = {"file": open(inputFile, "rb")}
    response = requests.post(url, files=file)
    file = open(outputFile, "wb")
    file.write(response.content)
    file.close()
    returnCode = response.status_code
    logging.info(returnCode)
    return outputFile


if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)
    logging.info("component can't run on its own")
