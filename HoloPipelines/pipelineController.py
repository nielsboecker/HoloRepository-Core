#TODO: list all pipelines(?) in json?
import json
import os

#how and where to get the json?
#docker commit to update the img everytime the list is appened     https://github.com/rocker-org/rocker/wiki/How-to-save-data    26/06/19
with open("pipelines.json") as json_file:
	lsPipe = json.load(json_file)
	#get id from a name of a pipeline?

#os.system('python file.py')