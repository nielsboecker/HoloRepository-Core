from flask import Flask, request
from pipelineController import startPipeline, getPipelineList
from flask_json import json_response
from datetime import datetime
from pathlib import Path
from pipelines.components.compStatus import status
from threading import Thread
from pipelines.components import compJobClean
from pipelines.components import compMapPipelineInfo
import uuid
import json
import logging
import os
import pathlib

app = Flask(__name__)
app.config["JSON_ADD_STATUS"] = False

# global variables
this_cwd = pathlib.Path.cwd()

output_directory = Path("output")
pipeline_list = getPipelineList()

jobid2plid = {"j0": "nifti2glb", "j1": "dicom2glb"}
job2inputURL = {"j0": "url"}
job2outputURL = {}


# logging formatting
FORMAT = "%(asctime)-15s -function name:%(funcName)s -%(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)


# update the status from pipeline
@app.route("/api/v1/status", methods=["POST"])
def update_job_status():
    global status
    current_job_status = request.get_json()
    current_jobID = list(current_job_status.keys())[0]
    status.update(current_job_status)
    logging.debug(
        "Get the current job status from status after update: "
        + json.dumps(status[current_jobID])
    )
    return json.dumps(status[current_jobID])


# get pipeline info
@app.route("/api/v1/pipelines", methods=["GET"])
def send_list_of_pipelines():
    global pipeline_list
    pipeline_dict = compMapPipelineInfo.map_pipelines_info()

    return json.dumps(pipeline_dict)


# use to start the pipeline
@app.route("/api/v1/job", methods=["POST"])
def start_job():

    # get the info from request
    job_request = request.get_json()
    request_plid = job_request["plid"]
    request_input_data_URL = job_request["imageStudyEndpoint"]

    # get filename
    if request_input_data_URL.find("/"):
        filename = request_input_data_URL.rsplit("/", 1)[1]
        logging.info("filename: " + filename)

    # create output dir
    global output_directory
    if not output_directory.is_dir():
        os.mkdir(output_directory)

    info_for_accessor = {
        "bodySite": job_request["bodySite"],
        "dateOfImaging": datetime.strptime(
            job_request["dateOfImaging"], "%Y-%m-%d %H:%M:%S"
        ).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "description": job_request["description"],
        "author": job_request["author"],
        "patient": job_request["patient"],
    }

    logging.info("info_for_accessor: " + json.dumps(info_for_accessor))

    # create arglist pass to pipeline controller
    # (this part will change later, we should not check the pipeline arglist in this way)
    jobID = str(uuid.uuid1())
    arg_dict = {
        "job_ID": jobID,
        "dicom_download_url": request_input_data_URL,
        "info_for_accessor": json.dumps(info_for_accessor),
    }
    logging.info("arg_dict: " + str(arg_dict))

    # pass to controller to start pipeline
    startPipeline(request_plid, arg_dict)
    return json_response(jobID=jobID, status_code=202)


@app.route("/api/v1/job/<jobid>/status", methods=["GET"])
def get_job_status(jobid):
    if jobid in status:
        current_status = status[jobid]["status"]
        return json_response(message=current_status, status_code=202)
    else:
        return json_response(message="does not exist", status_code=202)


if __name__ == "__main__":
    Thread(target=compJobClean.activate_status_cleaning_job).start()
    Thread(target=app.run, kwargs={"debug": False, "port": 3100}).start()
