# Uploading files
To use the server two directories for the prediction and uploaded files have to be created. The directories should be named *data* for uploads and *prediction* for the segmentation.

# Testing the flask server
Run the flask server:
```bash
python server.py
```

Once the server is up and running, the following command can be used to check if everything is working fine.
We post the three required input files against the server and save the output in a file called *segmentation.nii.gz*.
```bash
curl -F "file[]=@FLAIR.nii.gz" -F "file[]=@T1.nii.gz" -F "file[]=@IR.nii.gz" localhost:5000/model -o segmentation.nii.gz
```
