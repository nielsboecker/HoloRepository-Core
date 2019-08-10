from flask import Flask, request
from pipelineController import startPipeline, getPipelineList
from flask_json import json_response
from datetime import datetime
from pathlib import Path
from zipfile import ZipFile
import uuid
import json
import threading
import time
import logging
import requests
import os
import pathlib

app = Flask(__name__)
app.config["JSON_ADD_STATUS"] = False

# global variables
this_cwd = pathlib.Path.cwd()
save_directory = Path("input")
output_directory = Path("output")
pipeline_list = getPipelineList()
status = {
    "j0": {"status": "segment", "stamp": "2019-08-05 14:09:19"},
    "j1": {"status": "segment", "stamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
}
jobid2plid = {"j0": "nifti2glb", "j1": "dicom2glb"}
job2inputURL = {"j0": "url"}
job2outputURL = {}


# logging formatting
FORMAT = "%(asctime)-15s -function name:%(funcName)s -%(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT)


def save_request_file_to_input_dir(filename, request_input_data_URL):
    global save_directory
    if not save_directory.is_dir():
        os.mkdir("input")
    response = requests.get(request_input_data_URL)
    if response.status_code != 200:
        return json_response(jobID="image study endpoint failure", status_code=404)
    file_dir = this_cwd.joinpath(str(save_directory), filename)
    open(file_dir, "wb+").write(response.content)
    logging.info("file dir: " + str(file_dir))


def unzip_the_file(filename):
    # get unzip input filename
    filename_unzip = filename.rsplit(".", 1)[0]
    logging.info("unzip file name:" + filename_unzip)

    # unzip the input file
    file_dir = this_cwd.joinpath(str(save_directory), filename)
    path_to_store_unzip_file = this_cwd.joinpath(str(save_directory), filename_unzip)
    with ZipFile(str(file_dir), "r") as zipObj:
        # unzip
        zipObj.extractall(str(path_to_store_unzip_file))
    return str(path_to_store_unzip_file)


# cleaning the status
@app.before_first_request
def activate_status_cleaning_job():
    def run_job():
        while True:
            global status
            # logging.info("status before loop: " +str(status))

            for job in status.copy():

                job_time_string = status[job]["stamp"]
                # logging.info("job-time: "+job_time_string)

                job_time_obj = datetime.strptime(job_time_string, "%Y-%m-%d %H:%M:%S")

                current_time = datetime.now()
                delta_time = (current_time - job_time_obj).total_seconds()
                # logging.info("time difference: "+str(delta_time))

                # if job exists more than 30 mins delete it from dictionary
                if delta_time >= 1800.0:
                    status.pop(job)

            time.sleep(30)

    # logging.info("status after loop: "+str(status))
    thread = threading.Thread(target=run_job)
    thread.start()


# update the status from pipeline
@app.route("/api/v1/status", methods=["POST"])
def getTheStatus():

    global status
    current_job_status = request.get_json()
    status.update(current_job_status)
    return json.dumps(status)


# get pipeline info
@app.route("/api/v1/pipelines", methods=["GET"])
def send_list_of_pipelines():
    global pipeline_list
    pipeline_dict = {}
    for (
        key,
        value,
    ) in (
        pipeline_list.items()
    ):  # not complete. the value for inputConstraints is wrong (atm it's just number of param)
        pipeline_dict[key] = {
            "plid": key,
            "title": value["name"],
            "description": value["description"],
            "inputConstraints": value["inputConstraints"],
            "inputExampleImageUrl": value["inputExampleImageUrl"],
            "outputExampleImageUrl": value["outputExampleImageUrl"],
        }

    return json.dumps(pipeline_dict)  # should we str() here?


# use to start the pipeline
@app.route("/api/v1/job", methods=["POST"])
def send_job_start_response():

    # get the info from request
    job_request = request.get_json()
    request_plid = job_request["plid"]
    request_input_data_URL = job_request["imageStudyEndpoint"]

    # get filename
    if request_input_data_URL.find("/"):
        filename = request_input_data_URL.rsplit("/", 1)[1]
        logging.info("filename: " + filename)

    save_request_file_to_input_dir(filename, request_input_data_URL)
    unzip_file_dir = unzip_the_file(filename)

    # create output dir
    global output_directory
    if not output_directory.is_dir():
        os.mkdir("output")

    # create a list that fetch the response info that needs to post with hologram to the accessor (checking is missing)
    info_for_accesor = {
        "bodySite": job_request["bodySite"],
        "dateOfImaging": datetime.strptime(
            job_request["dateOfImaging"], "%Y-%m-%d %H:%M:%S"
        ).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "description": job_request["description"],
        "author": job_request["author"],
        "patient": job_request["patient"],
    }
    logging.info("info_for_accesor: " + json.dumps(info_for_accesor))

    # create arglist pass to pipeline controller
    # (this part will change later, we should not check the pipeline arglist in this way)
    jobID = str(uuid.uuid1())
    global jobid2plid
    jobid2plid.update({jobID: request_plid})
    if request_plid != "lungDicom2glb":
        arglist = [
            jobID,
            unzip_file_dir,
            str(
                this_cwd.joinpath(
                    str(output_directory), unzip_file_dir.rsplit("/", 1)[1] + ".glb"
                )
            ),
            "300",
            json.dumps(info_for_accesor),
        ]
    else:
        arglist = [
            jobID,
            unzip_file_dir,
            str(
                this_cwd.joinpath(
                    str(output_directory), unzip_file_dir.rsplit("/", 1)[1] + ".glb"
                )
            ),
            json.dumps(info_for_accesor),
        ]
    logging.info("arglist: " + str(arglist))

    # pass to controller to start pipeline
    startPipeline(jobID, request_plid, arglist)
    return json_response(jobID=jobID, status_code=202)


@app.route("/api/v1/job/<jobid>/status", methods=["GET"])
def get_job_status(jobid):
    if jobid in status:
        status_for_current_jobid = {jobid: status[jobid]["status"]}
    else:
        status_for_current_jobid = {jobid: "does not exist"}

    return json.dumps(status_for_current_jobid)


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1")
