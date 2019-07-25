from flask import Flask, request, send_file, url_for, escape, jsonify
from pipelineController import startPipeline
import json

app = Flask(__name__)

status={}
piprline={}

pipeline0={}
pipeline0["plid"]="p0"
pipeline0["paramlist"]=[]





@app.route('/status', methods=['POST'])
def get_the_status():
    #status=request.get_json()
    #status['job1']=app = Flask(__name__)
    #{
    # j1:{status: seapp = Flask(__name__)
    # j2:{}
    # }
    return jsonify({app = Flask(__name__)

@app.route('/pipelinapp = Flask(__name__)
def send_list_of_pipapp = Flask(__name__)

    # plid == p0
    # title == name
    # description == info
    # input constraint == ?
    # input sample imageurl ==?
    # output sample imageurl ==?

    return 'pipelines'


@app.route('/job',methods=['POST'])
def send_job_start_response():
    # 
    # pipeline id and arguments relate to the pipeline pipielineID=s0
    startPipeline(pipeline0["plid"],pipeline0["paramlist"])
    return 'jobid', 202

@app.route('/job/<jobid>/status',methods=['GET'])
def get_job_status(jobid):
    # show the user profile for that user


    return 'User %s' % escape(jobid)

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1")
