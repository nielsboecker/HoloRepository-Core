from flask import Flask, request
from pipelineController import startPipeline, getPipelineList
from flask_json import json_response
from datetime import datetime
from pathlib import Path
import uuid
import json
import threading
import time
import logging
import requests
import os
import pathlib
from zipfile import ZipFile

app = Flask(__name__)
this_cwd = pathlib.Path.cwd()
save_directory = Path("input")
pipeline_list = getPipelineList()
FORMAT = "%(asctime)-15s -function name:%(funcName)s -%(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT)

# status = {"j0":{ "status": "segment", "stamp":datetime.now().strftime('%Y-%m-%d %H:%M:%S') }}
status = {
    "j0": {"status": "segment", "stamp": "2019-08-05 14:09:19"},
    "j1": {"status": "segment", "stamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
}
app.config["JSON_ADD_STATUS"] = False
pipeline = {}


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
@app.route("/status", methods=["POST"])
def getTheStatus():

    global status
    current_job_status = request.get_json()
    status.update(current_job_status)
    return json.dumps(status)


# get pipeline info
@app.route("/pipelines", methods=["GET"])
def sendListOfPipapp():
    global pipeline_list
    pipelineDict = {}
    for (
        key,
        value,
    ) in (
        pipeline_list.items()
    ):  # not complete. the value for inputConstraints is wrong (atm it's just number of param)
        pipelineDict[key] = {
            "plid": key,
            "title": value["name"],
            "description": value["info"],
            "inputConstraints": value["param"],
            "inputExampleImageUrl": "NothingToSeeHere",
            "outputExampleImageUrl": "NothingToSeeHere",
        }

    return json.dumps(pipelineDict)  # should we str() here?


# use to start the pipeline
@app.route("/job", methods=["POST"])
def sendJobStartResponse():
    # get the request
    job_request = request.get_json()
    request_plid = job_request["pid"]
    request_input_data_URL = job_request["imagingStudyEndpoint"]
    if request_input_data_URL.find("/"):
        filename = request_input_data_URL.rsplit("/", 1)[1]
        logging.info("filename: " + filename)

    # save file to input file
    global save_directory
    if not save_directory.is_dir():
        os.mkdir("input")
    response = requests.get(request_input_data_URL)
    input_dir = "input"
    file_dir = this_cwd.joinpath(input_dir, filename)
    open(file_dir, "wb+").write(response.content)
    logging.info("file dir: " + str(file_dir))

    # get unzip input filename
    filename_unzip = filename.rsplit(".", 1)[0]
    logging.info("unzip file name:" + filename_unzip)

    # unzip the input file
    path_to_store_unzip_file = this_cwd.joinpath(filename_unzip)
    with ZipFile(str(file_dir), "r") as zipObj:  # unzip
        zipObj.extractall(str(path_to_store_unzip_file))

    jobID = str(uuid.uuid1())
    # arglist = [jobID, "input_for_PACS/" + filename_unzip]

    if pipeline_list[request_plid]["param"] == str(len(job_request["arglist"])):
        startPipeline(jobID, job_request["pid"], job_request["arglist"])
    return json_response(jobID=jobID, status_code=202)
    # else:
    # return json_response(jobID="", status_code=404)


@app.route("/job/<jobid>/status", methods=["GET"])
def getJobStatus(jobid):
    if jobid in status:
        status_for_current_jobid = {jobid: status[jobid]}
    else:
        status_for_current_jobid = {jobid: "does not exist"}

    return json.dumps(status_for_current_jobid)


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1")
