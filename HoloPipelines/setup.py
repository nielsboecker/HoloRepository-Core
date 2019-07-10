import urllib.request
from zipfile import ZipFile
import os
import pipelines.components.fileHandler as fileHand

saveto = os.getcwd()

print('Checking if dir exits...')

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



#download dcm zip
print('Beginning dicom sample download...')

url = 'https://holoblob.blob.core.windows.net/test/3_Axial_CE.zip'
urllib.request.urlretrieve(url, str(saveto) +fileHand.slash+ "__temp__.zip") 

print('Beginning dicom unzip...')
with ZipFile('__temp__.zip', 'r') as zipObj:
	zipObj.extractall(fileHand.dicomPath)
os.remove('__temp__.zip')

#download nifti
print('Beginning nifti sample download...')

url = 'https://holoblob.blob.core.windows.net/test/1103_3_glm.nii.zip'  
urllib.request.urlretrieve(url, str(saveto) +fileHand.slash+ "__temp__.zip") 

print('Beginning nifti unzip...')
with ZipFile('__temp__.zip', 'r') as zipObj:
	zipObj.extractall(fileHand.niftiPath)
os.remove('__temp__.zip')

print("setup: done")