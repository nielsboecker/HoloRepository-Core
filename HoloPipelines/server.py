import logging

import coloredlogs
from flask import Flask, request
from flask_json import as_json

from core.utils.pipelines_info import read_and_map_pipelines_info
from jobs import job_controller
from jobs.job_status import activate_periodic_garbage_collection, get_current_stage
from jobs.jobs_io import read_log_file_for_job

log_format = "%(asctime)s | %(name)s | %(levelname)s | %(message)s'"
coloredlogs.install(level=logging.DEBUG, fmt=log_format)

app = Flask(__name__)
app.config["JSON_ADD_STATUS"] = False
URL_API_PREFIX = "/api/v1"


@app.route(f"{URL_API_PREFIX}/pipelines", methods=["GET"])
@as_json
def get_pipelines():
    """
    :return: JSON List of available pipelines
    """
    pipeline_dict = read_and_map_pipelines_info()
    return pipeline_dict, 200


@app.route(f"{URL_API_PREFIX}/jobs", methods=["POST"])
@as_json
def start_new_job():
    """
    Starts a new job.
    :return: JSON response {jid: <job_id>} with according HTTP response code set
    """
    job_request = request.get_json()
    job_started_successfully, response = job_controller.start_new_job(job_request)
    response_code = 202 if job_started_successfully else 500
    return response, response_code


@app.route(f"{URL_API_PREFIX}/jobs/<job_id>/status", methods=["GET"])
@as_json
def get_job_status(job_id: str):
    """
    :return: JSON response {stage: <JobStage.name>} or {message: <error_message>} with
    according HTTP response code set
    """
    current_stage = get_current_stage(job_id)
    if current_stage:
        return {"stage": current_stage}, 200
    else:
        return {"message": f"Job '{job_id}' not found"}, 404


@app.route(f"{URL_API_PREFIX}/jobs/<job_id>/log", methods=["GET"])
def get_job_log(job_id: str):
    """
    :return: the complete log for a specific job as text
    """
    log_text = read_log_file_for_job(job_id)
    return log_text, 200


if __name__ == "__main__":
    activate_periodic_garbage_collection()
    # TODO: port shouldn't be hard-coded here
    app.run(debug=False, port=3100)
