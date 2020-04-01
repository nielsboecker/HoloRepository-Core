import os
from flask import Flask, request, send_file
from werkzeug.utils import secure_filename

from model import brain_model

import logging
import coloredlogs
log_format = "%(asctime)s | %(name)s | %(levelname)s | %(message)s'"
log_level = logging.INFO
coloredlogs.install(level=log_level, fmt=log_format)

logging.info("Running setup from server.py")

# The directory paths are given by the original model in the container
UPLOAD_FOLDER = "./data"
OUTPUT_FOLDER = "./prediction"

ALLOWED_EXTENSION = "nii.gz"

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["OUTPUT_FOLDER"] = OUTPUT_FOLDER


def file_format_is_allowed(filename):
    return "." in filename and filename.split(".", 1)[1].lower() == ALLOWED_EXTENSION


def filename_without_extension(filename):
    return filename.rsplit(".")[0]


@app.route("/model", methods=["POST"])
def seg_file():
    files = request.files.getlist("file[]")
    if len(files) != 3:
        return "Wrong number of files uploaded", 400
    for file in files:
        if file and file_format_is_allowed(file.filename):
            # save files in folder called upload
            filename = secure_filename(file.filename)
            # TODO check each file is uploaded once exactly
            if filename in ["FLAIR.nii.gz", "IR.nii.gz", "T1.nii.gz"]:
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            else:
                return "Unknown filename uploaded", 400
        else:
            return "file does not have required extension", 400

    # predict using model
    try:
        logging.info("Starting segmentation...")
        output_file_path = brain_model.predict(app.config["UPLOAD_FOLDER"], app.config["OUTPUT_FOLDER"])
        logging.info("Finished segmentation. Dispatching output.")
    except:
        logging.info("An error occured, while performing segmentation")
        return "An error occured, while performing segmentation", 500
    # segmentation can now be found in output folder titled segmented.nii.gz
    return send_file(output_file_path), 200


if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1", port=5002)