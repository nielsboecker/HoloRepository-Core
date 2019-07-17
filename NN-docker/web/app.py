import os
from flask import Flask, flash, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename


app = Flask(__name__)

UPLOAD_FOLDER = '/root/niftynet/data/dense_vnet_abdominal_ct'
OUTPUT_FOLDER = '/root/niftynet/models/dense_vnet_abdominal_ct/segmentation_output'
ALLOWED_EXTENSIONS = set(['nii'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER']= OUTPUT_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def output_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'],filename, as_attachment=True)


def output_filename(filename):
    filename_noextension=filename.split('_')[0]
    return filename_noextension+"__niftynet_out.nii.gz"

@app.route("/")
def hello_world():
    return "Hello World"

@app.route("/seg", methods=['POST','GET'])
def seg_file():
    if 'file' not in request.files:
        return 'No file in the request'

    file = request.files['file']

    if file.filename=='':
        return 'No selected file'

    if file.filename!='seg_CT.nii':
        file.filename='seg_CT.nii'

    if file and allowed_file(file.filename):
        filename=secure_filename(file.filename)
        print(filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        os.system('net_segment inference -c ~/niftynet/extensions/dense_vnet_abdominal_ct/config.ini')

        return send_file(OUTPUT_FOLDER+'/'+output_filename(filename))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
