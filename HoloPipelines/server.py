"""
This module represents the entrypoint of the HoloPipelines. It starts
a Flask server and listens to endpoints, allowing external clients to
start jobs and trace their progress.
"""

import logging
from typing import Tuple

import coloredlogs
from flask import Flask, request
from flask_json import as_json
from flask_cors import CORS

from config import FLASK_ENV, APP_PORT
from core.pipelines.pipelines_controller import get_pipelines_dict
from jobs import jobs_controller
from jobs.jobs_state import activate_periodic_garbage_collection, get_current_state
from jobs.jobs_io import read_log_file_for_job, init_create_job_state_root_directories

log_format = "%(asctime)s | %(name)s | %(levelname)s | %(message)s'"
log_level = logging.DEBUG if FLASK_ENV == "development" else logging.INFO
coloredlogs.install(level=log_level, fmt=log_format)

# Note: Code to run at import time, see https://stackoverflow.com/a/44406384/8495954
# When you run the server through gunicorn, the __main__ doesn't run, so to workaround
# puts the initialisation to the top level, invoking it at import time. This may be a 
# problem if/when we start gunicorn with multiple workers. If we keep gunicorn workers
# at 1, as we have now, and start multiple processes in our own code, it should be fine.
logging.info("Running setup from server.py")
init_create_job_state_root_directories()
activate_periodic_garbage_collection()

app = Flask(__name__)
app.config["JSON_ADD_STATUS"] = False
CORS(app)
URL_API_PREFIX = "/api/v1"


@app.route(f"{URL_API_PREFIX}/pipelines", methods=["GET"])
@as_json
def get_pipelines() -> Tuple[dict, int]:
    """
    :return: JSON List of available pipelines
    """
    return get_pipelines_dict(), 200


@app.route(f"{URL_API_PREFIX}/jobs", methods=["POST"])
@as_json
def start_new_job() -> Tuple[dict, int]:
    """
    Starts a new job.
    :return: JSON response {jid: <job_id>} with according HTTP response code set
    """
    job_request = request.get_json()
    job_started_successfully, response = jobs_controller.start_new_job(job_request)
    response_code = 202 if job_started_successfully else 500
    return response, response_code


@app.route(f"{URL_API_PREFIX}/jobs/<job_id>/state", methods=["GET"])
@as_json
def get_job_state(job_id: str) -> Tuple[dict, int]:
    """
    :return: JSON response {state: <JobState.name>} or {message: <error_message>} with
    according HTTP response code set
    """
    state, age = get_current_state(job_id)
    if state:
        return {"state": state, "age": age}, 200
    else:
        return {"message": f"Job '{job_id}' not found"}, 404


@app.route(f"{URL_API_PREFIX}/jobs/<job_id>/log", methods=["GET"])
def get_job_log(job_id: str) -> Tuple[str, int]:
    """
    :return: the complete log for a specific job as text
    """
    log_text = read_log_file_for_job(job_id)
    return log_text, 200


if __name__ == "__main__":
    app.run(debug=FLASK_ENV == "development", port=APP_PORT)
