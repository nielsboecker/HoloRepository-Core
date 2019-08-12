import requests
import pathlib


def send_file_post_request(url, input_file, output_file):
    inputFile = str(pathlib.Path(input_file))
    outputFile = str(pathlib.Path(output_file))
    file = {"file": open(inputFile, "rb")}
    response = requests.post(url, files=file)
    file = open(outputFile, "wb")
    file.write(response.content)
    file.close()
    returnCode = response.status_code
    print(returnCode)
    return outputFile


if __name__ == "__main__":
    print("component can't run on its own")
