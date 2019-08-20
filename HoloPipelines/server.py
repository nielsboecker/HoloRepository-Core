import json
import logging
from threading import Thread

import coloredlogs
from flask import Flask, request
from flask_json import as_json

from core.utils.pipelines_info import read_and_map_pipelines_info
from jobs import job_controller, job_status_garbage_collector
from jobs.job_status import status

log_format = "%(asctime)s [pid %(process)d] %(levelname)s | %(message)s'"
coloredlogs.install(level=logging.DEBUG, fmt=log_format)

app = Flask(__name__)
app.config["JSON_ADD_STATUS"] = False
URL_API_PREFIX = "/api/v1"


# TODO: Refactor or delete: Shouldn' be here at all. If we keep it, PUT instead...
@app.route(f"{URL_API_PREFIX}/status", methods=["POST"])
def update_job_status():
    current_job_status = request.get_json()
    current_jobID = list(current_job_status.keys())[0]
    status.update(current_job_status)
    logging.debug(
        "Get the current job status from status after update: "
        + json.dumps(status[current_jobID])
    )
    return json.dumps(status[current_jobID])


@app.route(f"{URL_API_PREFIX}/pipelines", methods=["GET"])
@as_json
def get_pipelines():
    pipeline_dict = read_and_map_pipelines_info()
    return pipeline_dict, 200


@app.route(f"{URL_API_PREFIX}/jobs", methods=["POST"])
@as_json
def start_new_job():
    job_request = request.get_json()
    job_started_successfully, response = job_controller.start_new_job(job_request)
    response_code = 202 if job_started_successfully else 500
    return response, response_code


@app.route(f"{URL_API_PREFIX}/jobs/<job_id>/status", methods=["GET"])
@as_json
def get_job_status(job_id: str):
    job_found, response = job_controller.get_job_status(job_id)
    response_code = 200 if job_found else 404
    return response, response_code


if __name__ == "__main__":
    Thread(target=job_status_garbage_collector.activate_status_cleaning_job).start()
    # TODO: Shouldn't be hard-coded here
    Thread(target=app.run, kwargs={"debug": False, "port": 3100}).start()
