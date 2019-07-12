import json
import os
import argparse
from subprocess import call as subpro
import pathlib

newCwd = str(pathlib.Path(str(os.path.dirname(os.path.realpath(__file__)))))

parser = argparse.ArgumentParser(description='Selct pipeline to process')
parser.add_argument('-l', '--ls', action="store_true", help="list all the available piplines")
parser.add_argument('-i', '--info', default = "", type=str, help="get info from pipeline's name")
parser.add_argument('pipelineID', type=str, nargs='?', help='ID of pipeline')
#parser.add_argument('pipelineID', type=str, nargs='?', help='ID of pipeline')
parser.add_argument('-p', '--param', default = [], nargs='*', help="parameters for pipeline e.g. dicom folder name or HU threshold")
args = parser.parse_args()

def main():
	searchCounter = 0
	with open(str(pathlib.Path(newCwd).joinpath("pipelines/pipelineList.json"))) as json_file:
		lsPipe = json.load(json_file)
		if args.ls:
			print(json.dumps(lsPipe, indent=4, sort_keys=False))
			exit()
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
			exit()

		temp = ""
		if args.pipelineID not in lsPipe:
			print("pipelineController: no pipeline with such ID")
			exit()
		if len(args.param) != int(lsPipe[args.pipelineID][0]['param']):#doesnt match with param req from json?
			print("pipelineController: invalid number of param [expected: " + str(lsPipe[args.pipelineID][0]['param']) + ", got: " + str(len(args.param)) + "]")
			exit()
		for i in args.param:
			temp = temp + str(i) + " "
		temp = temp[:len(temp) - 1]
		print("starting pipeline...")
		subpro('python ' + lsPipe[args.pipelineID][0]['src'] + " " + temp, cwd=newCwd, shell=True)

	json_file.close()

if __name__ == "__main__":
	main()