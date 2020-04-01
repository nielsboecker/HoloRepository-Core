import os
from flask import Flask, request, send_file
from model import kidney_model

# The directory paths are given by the original model in the container
UPLOAD_FOLDER = "./data"
OUTPUT_FOLDER = "./predictions"

ALLOWED_EXTENSION = "nii.gz"
MODEL_FILENAME = "imaging.nii.gz"

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["OUTPUT_FOLDER"] = OUTPUT_FOLDER

# model = kidney_model("kidney_model_miscnn", upload_folder=UPLOAD_FOLDER)


def file_format_is_allowed(filename):
    return "." in filename and filename.split(".", 1)[1].lower() == ALLOWED_EXTENSION


def filename_without_extension(filename):
    return filename.rsplit(".")[0]

@app.route("/model", methods=["POST"])
def seg_file():
    if "file" not in request.files:
        return "No file in the request", 400

    file = request.files["file"]

    if file.filename == "":
        return "No selected file", 400

    if file and file_format_is_allowed(file.filename):
        # save file in folder named after filename and image called imaging.nii
        foldername = filename_without_extension(file.filename)
        os.mkdir(os.path.join(app.config["UPLOAD_FOLDER"], foldername))
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], foldername, MODEL_FILENAME))
        # predict using model
        kidney_model.predict(foldername, app.config["OUTPUT_FOLDER"])
        # segmentation can now be found in output folder with the original filename
        return send_file(app.config["OUTPUT_FOLDER"] + "/" + file.filename), 200
    else:
        return "file does not have required extension", 400


if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1")
