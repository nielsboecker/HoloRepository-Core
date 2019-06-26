#TODO: list all pipelines(?) in json?
#TODO: add sample.py to test out pipeline
import json
import os

#how and where to get the json?
#docker commit to update the img everytime the list is appened     https://github.com/rocker-org/rocker/wiki/How-to-save-data    26/06/19
with open("json/pipelineList.json") as json_file:
	lsPipe = json.load(json_file)
	#get id from a name of a pipeline?

#os.system('python file.py')