import requests
import pathlib


def send_file_post_request(url, input_file, output_file):
    input_file = str(pathlib.Path(input_file))
    output_file = str(pathlib.Path(output_file))
    file = {"file": open(input_file, "rb")}
    response = requests.post(url, files=file)
    file = open(output_file, "wb")
    file.write(response.content)
    file.close()
    returnCode = response.status_code
    print(returnCode)
    return output_file


if __name__ == "__main__":
    print("component can't run on its own")
