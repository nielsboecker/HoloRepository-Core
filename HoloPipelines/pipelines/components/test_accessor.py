from compHttpRequest import sendFilePostRequestToAccessor

url="http://localhost:3200"
directory="/home/kawai/git/HoloRepository-Core/HoloPipelines/output/left-scfe-pelvis-bone.glb"
author={
    "aid":"123",
    "name": {
               "full":"Kawai Wong",
               "title": "Mr",
               "given": "Kawai",
               "family": "Wong"
            }
  }
patient={
    "pid":"321",
    "name": {
              "full":"Andy Lau",
              "title": "Mr",
              "given": "Andy",
              "family": "Lau"
            }
  }


sendFilePostRequestToAccessor("pelvis generate from dicom to glb",url,directory,"pelvis bone gernerate from dicom to glb pipeline","hip","2017-07-15T15:20:25Z","2017-07-15T15:20:25Z","pelvis generate from dicom2glb",author,patient)