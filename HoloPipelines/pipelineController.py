import json
import os
import sys
import argparse
import subprocess
import pathlib

newCwd = str(pathlib.Path(str(os.path.dirname(os.path.realpath(__file__)))))

parser = argparse.ArgumentParser(description="Selct pipeline to process")
parser.add_argument(
    "-c",
    "--config",
    default="./pipelineList.json",
    type=str,
    help="path to pipeline config file relative to pipelineController",
)
parser.add_argument(
    "-l", "--ls", action="store_true", help="list all the available piplines"
)
parser.add_argument(
    "-i", "--info", default="", type=str, help="get info from pipeline's name"
)
parser.add_argument("pipelineID", type=str, nargs="?", help="ID of pipeline")
parser.add_argument(
    "-p",
    "--param",
    default=[],
    nargs="*",
    help="parameters for pipeline e.g. dicom folder name or HU threshold",
)
args = parser.parse_args()


def main():
    # check common dir
    if not os.path.exists("medicalScans"):
        os.mkdir("medicalScans")
        os.mkdir("medicalScans/dicom")
        os.mkdir("medicalScans/nifti")
    if not os.path.exists("output"):
        os.mkdir("output")
        os.mkdir("output/OBJ")
        os.mkdir("output/GLB")

    # check for pipeline config file
    if not os.path.exists(str(pathlib.Path(newCwd).joinpath(str(args.config)))):
        sys.exit("error: config file not found")

    searchCounter = 0
    with open(str(pathlib.Path(newCwd).joinpath(str(args.config)))) as json_file:
        lsPipe = json.load(json_file)
        # --ls flag
        if args.ls:
            print(json.dumps(lsPipe, indent=4, sort_keys=False))
            sys.exit()
        if args.info:
            for key, value in lsPipe.items():
                data = value
                if args.info in data["name"]:
                    print("**ID: " + key)
                    print("name: " + data["name"])
                    print("source: " + data["src"])
                    print("param req: " + data["param"])
                    print("description: " + data["info"])
                    print("date added: " + data["addDate"])
                    print("date last modified: " + data["modDate"])
                    print("")
                    searchCounter += 1
            if searchCounter == 0:
                sys.exit("pipelineController: no pipeline with such name")
            else:
                print("pipelineController: " + str(searchCounter) + " results")
            sys.exit()
        # check if pipeline exist
        if args.pipelineID not in lsPipe:
            sys.exit("pipelineController: no pipeline with such ID")
        if len(args.param) != int(lsPipe[args.pipelineID]["param"]):
            sys.exit(
                "pipelineController: invalid number of param [expected: "
                + str(lsPipe[args.pipelineID]["param"])
                + ", got: "
                + str(len(args.param))
                + "]"
            )
        # start pipeline
        print("starting pipeline " + args.pipelineID + "...")
        subprocess.run(
            ["python", lsPipe[args.pipelineID]["src"]] + args.param, cwd=newCwd
        )

    json_file.close()


if __name__ == "__main__":
    main()
