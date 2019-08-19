import logging
from datetime import datetime

# TODO: Refactor (or remove, if we only do the logging to file?)
from enum import Enum

from core.clients.http import send_post_to_status

status = {
    "j0": {"status": "segment", "timestamp": "2019-08-05 14:09:19"},
    "j1": {
        "status": "segment",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    },
}


# TODO: Refactor this whole thing
# TODO: when using for update_job, pass the enum not the sting value
# TODO: sort them to be chronological
class JobStatus(Enum):
    STARTING = 1
    PREPROCESSING = 2
    GENERATING_MODEL = 3
    CONVERTING_MODEL = 4
    FINISHED = 5
    FETCHING_DATA = 6


# TODO: Moved from compJobStatus. A bit ugly to have this here, but ideally we can get rid of the self-POSTing altogether
def post_status_update(job_ID, job_status):
    data = {job_ID: {"status": job_status, "timestamp": str(datetime.now())}}
    response = send_post_to_status(data)
    return_code = response.status_code
    logging.debug("return code: " + str(return_code))
