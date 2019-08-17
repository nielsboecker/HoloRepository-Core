import json
import os
import sys
import argparse
import subprocess
import pathlib
import logging
import importlib
from pipelines.components.compGetPipelineListInfo import get_pipeline_list

from multiprocessing import Process
import pipelines.components.compCommonPath as pl_common_path


FORMAT = "%(asctime)-15s -function name:%(funcName)s -%(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT)


new_cwd = str(pathlib.Path(str(os.path.dirname(os.path.realpath(__file__)))))


parser = argparse.ArgumentParser(description="Select pipeline to process")
parser.add_argument(
    "-c",
    "--config",
    default="pipelineList.json",
    type=str,
    help="path to pipeline config file relative to pipelineConfig",
)
parser.add_argument(
    "-l", "--ls", action="store_true", help="list all the available piplines"
)
parser.add_argument(
    "-i",
    "--info",
    default="",
    metavar="NAME",
    type=str,
    help="get info from pipeline's name",
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

    pl_common_path.main()

    # check for pipeline config file
    if not os.path.exists(str(pathlib.Path(new_cwd).joinpath(str(args.config)))):
        sys.exit("error: config file not found")

    search_counter = 0
    with open(str(pathlib.Path(new_cwd).joinpath(str(args.config)))) as json_file:
        list_of_pipeline = json.load(json_file)
        # --ls flag
        if args.ls:
            logging.info(json.dumps(list_of_pipeline, indent=4, sort_keys=False))
            sys.exit()
        if args.info:

            for key, value in list_of_pipeline.items():
                data = value
                if args.info in data["name"]:
                    logging.info("**ID: " + key)
                    logging.info("name: " + data["name"])
                    logging.info("source: " + data["src"])
                    logging.info("param req: " + data["param"])
                    logging.info("description: " + data["info"])
                    logging.info("date added: " + data["addDate"])
                    logging.info("date last modified: " + data["modDate"])
                    logging.info("")
                    search_counter += 1
            if search_counter == 0:
                sys.exit("pipelineConfig: no pipeline with such name")

            else:
                logging.info("pipelineConfig: " + str(search_counter) + " results")
            sys.exit()
        # check if pipeline exist
        if args.pipelineID not in list_of_pipeline:
            sys.exit("pipelineConfig: no pipeline with such ID")
        if len(args.param) != int(list_of_pipeline[args.pipelineID]["param"]):
            sys.exit(
                "pipelineConfig: invalid number of param [expected: "
                + str(list_of_pipeline[args.pipelineID]["param"])
                + ", got: "
                + str(len(args.param))
                + "]"
            )
        # start pipeline
        logging.info("starting pipeline " + args.pipelineID + "...")
        subprocess.run(
            ["python", list_of_pipeline[args.pipelineID]["src"]] + args.param,
            cwd=new_cwd,
        )

    json_file.close()


def startPipeline(pipeline_ID, parameter_dict):
    list_of_pipeline = get_pipeline_list()
    list_of_pipeline[pipeline_ID]["src"].split(".py")[0].replace("/", ".")
    pl_package_name = (
        list_of_pipeline[pipeline_ID]["src"].split(".py")[0].replace("/", ".")
    )
    pl_package = importlib.import_module(pl_package_name)

    process = Process(target=pl_package.main, kwargs=(parameter_dict))
    process.start()
    # process.join


def dynamicLoadingPipeline(plID, parameter_dict):
    list_of_pipeline = get_pipeline_list()
    list_of_pipeline[plID]["src"].split(".py")[0].replace("/", ".")
    pl_package_name = list_of_pipeline[plID]["src"].split(".py")[0].replace("/", ".")
    pl_package = importlib.import_module(pl_package_name)
    pl_package.main(**parameter_dict)


if __name__ == "__main__":
    main()
