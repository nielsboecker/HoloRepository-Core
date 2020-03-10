# TODO README

### Command to test flask server
```bash
curl -F "files[]=@FLAIR.nii.gz" -F "files[]=@T1.nii.gz" -F "files[]=@IR.nii.gz" localhost:5000/model -o test.nii.gz
```