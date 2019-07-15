import json
import os
import sys
import argparse
from subprocess import call as call
import pathlib

newCwd = str(pathlib.Path(str(os.path.dirname(os.path.realpath(__file__)))))

parser = argparse.ArgumentParser(description='Selct pipeline to process')
parser.add_argument('-c', '--config', default = "pipelines/pipelineList.json", type=str, help="path to pipeline config file relative to pipelineController")
parser.add_argument('-l', '--ls', action="store_true", help="list all the available piplines")
parser.add_argument('-i', '--info', default = "", type=str, help="get info from pipeline's name")
parser.add_argument('pipelineID', type=str, nargs='?', help='ID of pipeline')
parser.add_argument('-p', '--param', default = [], nargs='*', help="parameters for pipeline e.g. dicom folder name or HU threshold")
args = parser.parse_args()

def main():
	if not os.path.exists("medicalScans"):
		os.mkdir("medicalScans")
		os.mkdir("medicalScans/dicom")
		os.mkdir("medicalScans/nifti")
	if not os.path.exists("numpy"):
		os.mkdir("numpy")
	if not os.path.exists("output"):
		os.mkdir("output")
		os.mkdir("output/OBJ")
		os.mkdir("output/GLB")
	if not os.path.exists("pipelines/components/lungSegment/result"):
		os.mkdir("pipelines/components/lungSegment/result")

	if not os.path.exists(str(pathlib.Path(newCwd).joinpath(str(args.config)))):
		sys.exit("error: config file not found")

	searchCounter = 0
	with open(str(pathlib.Path(newCwd).joinpath(str(args.config)))) as json_file:
		lsPipe = json.load(json_file)
		if args.ls:
			print(json.dumps(lsPipe, indent=4, sort_keys=False))
			sys.exit()
		elif len(args.info) > 0:
			for k, v in lsPipe.items():
				data = v[0]
				if args.info in data['name']:
					print("**ID: " + k)
					print("name: " + data["name"])
					print("source: " + data["src"])
					print("param req: " + data["param"])
					print("description: " + data["info"])
					print("date added: " + data["addDate"])
					print("date last modified: " + data["modDate"])
					print("")
					searchCounter=searchCounter + 1
			if searchCounter == 0:
				print("pipelineController: no pipeline with such name")
			else:
				print("pipelineController: "+str(searchCounter)+" results")
			sys.exit()

		temp = ""
		if args.pipelineID not in lsPipe:
			sys.exit("pipelineController: no pipeline with such ID")
		if len(args.param) != int(lsPipe[args.pipelineID][0]['param']):
			sys.exit("pipelineController: invalid number of param [expected: " + str(lsPipe[args.pipelineID][0]['param']) + ", got: " + str(len(args.param)) + "]")
		for i in args.param:
			temp = temp + str(i) + " "
		temp = temp[:len(temp) - 1]
		print("starting pipeline...")
		call('python ' + lsPipe[args.pipelineID][0]['src'] + " " + temp, cwd=newCwd, shell=True)

	json_file.close()

if __name__ == "__main__":
	main()