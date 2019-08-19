import json
import logging
import uuid
from datetime import datetime
from threading import Thread

import coloredlogs
from flask import Flask, request
from flask_json import as_json

from core.utils.pipelines_info import read_and_map_pipelines_info
from jobs import job_status_garbage_collector
from jobs.job_status import status
from pipeline_runner import startPipeline

coloredlogs.install()
logging.basicConfig(level=logging.DEBUG)

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


@app.route(f"{URL_API_PREFIX}/job", methods=["POST"])
@as_json
def start_job():
    job_request = request.get_json()
    request_plid = job_request["plid"]
    request_input_data_URL = job_request["imageStudyEndpoint"]

    # get filename
    if request_input_data_URL.find("/"):
        filename = request_input_data_URL.rsplit("/", 1)[1]
        logging.info("filename: " + filename)

    meta_data_keys = ["bodySite", "description", "author", "patient"]
    meta_data = {key: job_request[key] for key in meta_data_keys}
    meta_data["dateOfImaging"] = datetime.strptime(
        job_request["dateOfImaging"], "%Y-%m-%d %H:%M:%S"
    ).strftime("%Y-%m-%dT%H:%M:%SZ")
    logging.info("meta_data: " + json.dumps(meta_data))

    # create arglist pass to pipeline controller
    # (this part will change later, we should not check the pipeline arglist in this way)
    jobID = str(uuid.uuid1())
    arg_dict = {
        "job_ID": jobID,
        "dicom_download_url": request_input_data_URL,
        "meta_data": json.dumps(meta_data),
    }
    logging.info("arg_dict: " + str(arg_dict))

    # pass to controller to start pipeline
    startPipeline(request_plid, arg_dict)
    return {"jobID": jobID}, 202


@app.route(f"{URL_API_PREFIX}/job/<job_id>/status", methods=["GET"])
@as_json
def get_job_status(job_id: str):
    if job_id in status:
        current_status = status[job_id]["status"]
        return {"message": current_status}, 200
    else:
        return {"message": f"Job ID '{job_id}' not found"}, 404


if __name__ == "__main__":
    Thread(target=job_status_garbage_collector.activate_status_cleaning_job).start()
    # TODO: Shouldn't be hard-coded here
    Thread(target=app.run, kwargs={"debug": False, "port": 3100}).start()
