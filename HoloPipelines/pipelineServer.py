from flask import Flask, request, send_file, url_for, escape, jsonify
from pipelineController import startPipeline, getPipelineList
from flask_json import FlaskJSON, JsonError, json_response, as_json
import pathlib, os, sched, time, uuid, json, threading


app = Flask(__name__)

status = {"j0":{ "status": "segment", "stamp": "2020"}}
app.config["JSON_ADD_STATUS"] = False
pipeline = {}
jobID = ""

# cleaning the status
@app.before_first_request
def activate_status_cleaning_job():
    def run_job():
        while True:
            global status
            status={}
            print(status)
            time.sleep(5)

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
    job_request=request.get_json()
    request_plid=job_request["plid"]
    global jobID
    jobID = str(uuid.uuid1())
    print(len(job_request["arglist"]))

    if(pipelineList[request_plid]["param"]==str(len(job_request["arglist"]))):
       startPipeline(jobID, job_request["plid"],job_request["arglist"])
       return json_response(jobID=jobID, statuscode=202)
    else:
       return json_response(jobID="", statuscode=404)
    

# front end request the status
@app.route("/job/<jobid>/status", methods=["GET"])
def getJobStatus(jobid):
    if jobid in status:
        status_for_current_jobid={jobid:status[jobid]}
    else:
        status_for_current_jobid={jobid:"does not exist"} 

    return json.dumps(status_for_current_jobid)


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1")