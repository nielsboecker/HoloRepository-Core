from datetime import datetime
import logging
from pipelines.components.compHttpRequest import send_post_to_status

FORMAT = "%(asctime)-15s -function name:%(funcName)s -%(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)


def update_status(job_ID, job_status):
    data = {job_ID: {"status": job_status, "timestamp": str(datetime.now())}}
    response = send_post_to_status(data)
    return_code = response.status_code
    logging.debug("return code: " + str(return_code))


if __name__ == "__main__":
    print(
        "You shouldn't be able to run this component directly"
    )  # TODO look at this too pls
