#TODO: list all pipelines(?) in json?
#TODO: add sample.py to test out pipeline
#what do we do with the id?
import json
import os

#how and where to get the json?
#docker commit to update the img everytime the list is appened	 https://github.com/rocker-org/rocker/wiki/How-to-save-data	26/06/19
with open("json/pipelineList.json") as json_file:
	lsPipe = json.load(json_file)
	#print(lsPipe["s0"])
	#get id from a name of a pipeline?
	for k, v in lsPipe.items():
		data = v[0]
		#print(type(data))
		if data['name'] == 'sample0':#change to user input soon pls
			print("ID is: " + k)
			os.system('python %s' % data['src'])
			break

#os.system('python file.py')