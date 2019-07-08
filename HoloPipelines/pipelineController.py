import json
import os
import argparse

parser = argparse.ArgumentParser(description='Selct pipeline to process')
parser.add_argument('-l', '--ls', action="store_true", help="list all the available piplines")
parser.add_argument('-i', '--info', default = "", type=str, help="get info from pipeline's name")
parser.add_argument('src', type=str, nargs='?', help='input directory for medical image (folder for Dicom or .nii file)')
parser.add_argument('pipelineID', type=str, nargs='?', help='ID of pipeline')
parser.add_argument('-p', '--param', default = [], nargs='*', help="parameters for pipeline")
args = parser.parse_args()

with open("pipelines/pipelineList.json") as json_file:
	lsPipe = json.load(json_file)
	if args.ls:
		print(json.dumps(lsPipe, indent=4, sort_keys=False))
		exit()
	elif len(args.info) > 0:
		for k, v in lsPipe.items():
			data = v[0]
			if data['name'] == args.info:
				print("**ID: " + k)
				print("name: " + data["name"])
				print("source: " + data["src"])
				print("param req: " + data["param"])
				print("description: " + data["info"])
				print("date added: " + data["addDate"])
				print("date last modified: " + data["modDate"])
		exit()

	temp = ""
	#if len(args.param) doesnt match with param req from json?
	for i in args.param:
		temp = temp + str(i) + " "
	temp = temp[:len(temp) - 1]
	print("starting task...")
	os.system('python ' + lsPipe[args.src][0]['src'] + " " + temp)

json_file.close()