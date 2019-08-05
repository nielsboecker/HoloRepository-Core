from flask import Flask, request
from pipelineController import startPipeline, getPipelineList
from flask_json import json_response
from datetime import datetime
import uuid
import json
import threading
import time

app = Flask(__name__)

# status = {"j0":{ "status": "segment", "stamp":datetime.now().strftime('%Y-%m-%d %H:%M:%S') }}
status = {
    "j0": {"status": "segment", "stamp": "2019-08-05 14:09:19"},
    "j1": {"status": "segment", "stamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
}
app.config["JSON_ADD_STATUS"] = False
pipeline = {}
jobID = ""

# cleaning the status
@app.before_first_request
def activate_status_cleaning_job():
    def run_job():
        while True:
            global status
            # print("initial status: "status)

            for job in status.copy():

                job_time_string = status[job]["stamp"]
                # print("job time in sting: "+job_time_string)

                job_time_obj = datetime.strptime(job_time_string, "%Y-%m-%d %H:%M:%S")
                # print("job time in obj: "+str(job_time_obj))

                current_time = datetime.now()
                delta_time = (current_time - job_time_obj).total_seconds()
                # print("time difference: "+str(delta_time))

                if delta_time >= 1800.0:
                    status.pop(job)
            # print("status: "+str(status))
            time.sleep(30)

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

    # plid == p0
    # title == name
    # description == info
    # input constraint == ?
    # input sample imageurl ==?
    # output sample imageurl ==?

    pipelineList = getPipelineList()
    pipelineDict = {}
    for (
        key,
        value,
    ) in (
        pipelineList.items()
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
    pipelineList = getPipelineList()
    job_request = request.get_json()
    request_plid = job_request["plid"]
    global jobID
    jobID = str(uuid.uuid1())
    print(len(job_request["arglist"]))

    if pipelineList[request_plid]["param"] == str(len(job_request["arglist"])):
        startPipeline(jobID, job_request["plid"], job_request["arglist"])
        return json_response(jobID=jobID, statuscode=202)
    else:
        return json_response(jobID="", statuscode=404)


# front end request the status
@app.route("/job/<jobid>/status", methods=["GET"])
def getJobStatus(jobid):
    if jobid in status:
        status_for_current_jobid = {jobid: status[jobid]}
    else:
        status_for_current_jobid = {jobid: "does not exist"}

    return json.dumps(status_for_current_jobid)


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1")
