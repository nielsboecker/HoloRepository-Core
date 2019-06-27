#TODO: list all pipelines(?) in json?
#TODO: add sample.py to test out pipeline
#component installer? api?
#what do we do with the id?
import json
import os
import argparse#change to this when almost done. rn lrts just assume that all users know the id of the pipeline they wanna use.


parser = argparse.ArgumentParser(description='Selct pipeline to process')
parser.add_argument('-l', '--ls', action="store_true", help="list all the available piplines")
parser.add_argument('-i', '--info', default = "", type=str, help="get info from pipeline's name")
parser.add_argument('src', type=str, nargs='?', help='input directory for medical image (folder for Dicom or .nii file)')
parser.add_argument('pipelineID', type=str, nargs='?', help='ID of pipeline')#the piprline can decide the output
parser.add_argument('-p', '--param', default = [], nargs='*', help="parameters for pipeline")#default wasnt there b4
args = parser.parse_args()



#how and where to get the json?
#docker commit to update the img everytime the list is appened	 https://github.com/rocker-org/rocker/wiki/How-to-save-data	26/06/19
with open("json/pipelineList.json") as json_file:
	lsPipe = json.load(json_file)
	if args.ls:
		print(json.dumps(lsPipe, indent=4, sort_keys=False))
		exit()
		#return lsPipe
	elif len(args.info) > 0:
		for k, v in lsPipe.items():
			data = v[0]
			if data['name'] == args.info:#change to user input soon pls
				print("**ID: " + k)
				print("name: " + data["name"])
				print("source: " + data["src"])
				print("param req: " + data["param"])
				print("description: " + data["info"])
				print("date added: " + data["addDate"])
				print("date last modified: " + data["modDate"])
		exit()

	os.system('python %s' % lsPipe[args.src][0]['src'])#need to change this!!!!!!

	#print(lsPipe["s0"])
	#get id from a name of a pipeline?
	'''for k, v in lsPipe.items():
		data = v[0]
		#print(type(data))
		if str(k) == args.src:#change to user input soon pls
			print("ID is: " + k)
			os.system('python %s' % data['src'])
			break'''
json_file.close()

#os.system('python file.py')