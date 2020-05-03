import os
from flask import Flask, request, send_file
from werkzeug.utils import secure_filename
# import your model here
from model import template_model


app = Flask(__name__)

# The directory paths are given by the original model in the container (change these if necessary)
UPLOAD_FOLDER = "/root/upload_path"
OUTPUT_FOLDER = "/root/output_path"

# Specify the allowed file extension here
ALLOWED_EXTENSION = "nii"

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["OUTPUT_FOLDER"] = OUTPUT_FOLDER


def file_format_is_allowed(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() == ALLOWED_EXTENSION


@app.route("/model", methods=["POST"])
def seg_file():
    if "file" not in request.files:
        return "No file in the request", 400

    file = request.files["file"]

    if file.filename == "":
        return "No selected file", 400

    if file and file_format_is_allowed(file.filename):
        filename = secure_filename(file.filename)
        # Save posted file at specified path
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        # Use your model here for segmentation
        template_model.predict(app.config["UPLOAD_FOLDER"], app.config["OUTPUT_FOLDER"])

        # Return segmentation file
        return send_file(OUTPUT_FOLDER + "/" + filename), 200


if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1")
