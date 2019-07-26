from flask import Flask, request, send_file, url_for, escape, jsonify
from pipelineController import startPipeline, getPipelineList
import json
from flask_json import FlaskJSON, JsonError, json_response, as_json

app = Flask(__name__)

status = {"jobID": "j0", "status": "hey", "stamp": "2020"}
app.config["JSON_ADD_STATUS"] = False
piprline = {}

jobID = 0
pipeline0 = {}
pipeline0["plid"] = "p1"
pipeline0["paramlist"] = [
    "/Users/apple/Desktop/newholo/HoloRepository-Core/HoloPipelines/medicalScans/nifti/1103_3_glm.nii",
    "/Users/apple/Desktop/newholo/HoloRepository-Core/HoloPipelines/output/GLB/testtes.glb",
    "10",
]


@app.route("/status", methods=["POST"])
def get_the_status():
    global status
    current_job_status = request.get_json()
    status.update(current_job_status)
    return json.dumps(status)


@app.route("/pipelinapp", methods=["GET"])
def send_list_of_pipapp():

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


@app.route("/job", methods=["POST"])
def send_job_start_response():
    #
    # pipeline id and arguments relate to the pipeline pipielineID=s0
    global jobID
    jobID += 1
    startPipeline(str(jobID), pipeline0["plid"], pipeline0["paramlist"])
    return json_response(jobID=jobID, status=202)


@app.route("/job/<jobid>/status", methods=["GET"])
def get_job_status(jobid):
    # show the user profile for that user

    return "User %s" % escape(jobid)


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1")
